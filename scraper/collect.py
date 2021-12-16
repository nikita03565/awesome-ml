import datetime
import json
import os
import time
from pathlib import Path

import requests
import yaml

from scraper.utils import get_logger, default_headers, extract_articles

logger = get_logger(__name__)

# In days query parameters 943 stands for 1 Aug 2010 and 4815 -- 8 March 2021
search_url = "https://pikabu.ru/search?d={day_start}&D={day_end}&page={page}"

# Long stories
search_with_tag_url = "https://pikabu.ru/tag/%D0%94%D0%BB%D0%B8%D0%BD%D0%BD%D0%BE%D0%BF%D0%BE%D1%81%D1%82?d={day_start}&D={day_end}&page={page}"

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
output_dir = os.path.join(parent_dir, "data", "json")

config_path = os.path.join(parent_dir, "scraper", "config.yaml")
config = yaml.safe_load(open(config_path))
collect_config = config["collect"]
file_name = "{start}_{end}_{page}.json"
days_step = 1
earliest_date = 943

default_start = (datetime.date.today() - datetime.date(2010, 8, 1)).days + 943


def start_scraper():
    """
    This function requests html page from a given url in a loop,
    extracts content of <article> tag and saves result as a list in json file.
    """
    max_iterations = int(collect_config.get("max_iterations", 10))
    Path(output_dir).mkdir(exist_ok=True)
    session = requests.session()
    session.headers.update(default_headers)

    countdown_start = int(collect_config.get("countdown_start", 0)) or default_start

    # We might want to continue from the date that we have stopped on.
    # Find the least start date from existing files for that
    files = sorted(os.listdir(output_dir))
    if files and collect_config.get("continue_from_files"):
        countdown_start = int(files[0].split("_")[0])

    start = countdown_start - days_step
    end = countdown_start - 1
    n_iterations = 0
    while start > earliest_date:
        logger.debug(f"Searching in {start} - {end} range")
        for page in range(1, 100):
            if max_iterations and n_iterations > max_iterations:
                # THIS WAS MADE FOR TESTING PURPOSES ONLY
                raise SystemExit
            n_iterations += 1
            url = search_with_tag_url.format(day_start=start, day_end=end, page=page)
            logger.debug(f"Sending request to {url}")
            try:
                r = session.get(url, timeout=10)
            except Exception as e:
                logger.debug(f"Request ended with error: {e}")
                time.sleep(10)
                continue
            time.sleep(1)
            if r.status_code != 200:
                logger.debug(f"Got not 200 status code. Abort")
                return
            articles = extract_articles(r.text)
            if len(articles) == 0:
                # Stop iterating through pages and move to next days range
                logger.debug(f"No posts on the page")
                break
            f_name = file_name.format(start=start, end=end, page=page)
            with open(os.path.join(output_dir, f_name), "w", encoding="utf-8") as f:
                f.write(json.dumps(articles))
                logger.debug(f"Saved results in {os.path.join(output_dir, f_name)}")
        start = start - days_step
        end = end - days_step


if __name__ == "__main__":
    start_scraper()
