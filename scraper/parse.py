import json
import os
import re
from csv import DictWriter
from pathlib import Path

from lxml.html import fromstring
from tqdm import tqdm

MIN_CHARS = 2000

dir_name = "results"
output_dir = "parsed"


def clean(s):
    """
    Cleans given string from non-relevant information: links, punctuation, etc.
    :param s: raw string
    :return: cleaned string
    """
    s = re.sub(r"https\S+", " ", s)
    s = re.sub(r"^\s+|\n|\r|\t|\s+$", " ", s)
    s = re.sub(r"[^\w\s\d]", " ", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.lower().strip()


def get_dtm(el):
    dtm_el = el.xpath("//article//time")
    if dtm_el:
        return dtm_el[0].attrib.get("datetime")
    return None


def get_saves(el):
    saves_el = el.xpath("//article//div[contains(@class, 'story__save')]")
    if saves_el:
        # looks like "Сохранило 12 человек"
        label = saves_el[0].attrib.get("aria-label")
        splitted = label.split(" ")
        if len(splitted) == 3:
            try:
                return int(splitted[1])
            except ValueError:
                return None
    return None


def get_views(el):
    views_span = el.xpath("//article//span[contains(@class, 'story__views-count')]")
    span_value = None
    if views_span:
        span_value = views_span[0].attrib.get("aria-label")
    views_div = el.xpath("//article//div[contains(@class, 'story__views')]")
    div_value = None
    if views_div:
        # looks like "21 599 просмотров"
        # but there is a lot of divs with "Загружаем количество просмотров" value. So we can't get the views
        value = views_div[0].attrib.get("aria-label")
        try:
            value = value.replace("просмотров", "").replace(" ", "")
            div_value = int(value)
        except ValueError:
            div_value = None
    return span_value or div_value


def parse_post(el):
    """
    Extracts data from lxml's html element object.
    :param el: lxml html element object
    """
    text_elements = el.xpath("//article//div[contains(@class, 'story-block story-block_type_text')]")
    text = " ".join(" ".join(t.xpath("./*/text()")) for t in text_elements)
    if len(text) < MIN_CHARS:
        # No need to clean text if it already hasn't enough of characters
        return None
    cleaned_text = clean(text)
    if len(cleaned_text) < MIN_CHARS:
        return None
    tags_elements = el.xpath("//article//div[contains(@class, 'story__tags')]/a")
    return {
        "id": el.attrib["data-story-id"],
        "data-story-long": el.attrib["data-story-long"],
        "rating": el.attrib.get("data-rating"),
        "meta-rating": el.attrib["data-meta-rating"],
        "author_id": el.attrib["data-author-id"],
        "comments": el.attrib["data-comments"],
        "dtm": get_dtm(el),
        "saves": get_saves(el),
        "views": get_views(el),
        "author_name": el.xpath("//header//a[contains(@class, 'user__nick')]")[0].text_content().strip(),
        "title": el.xpath("//header//h2/a")[0].text_content().replace("\xc2\xa0", " ").replace("\xa0", " ").strip(),
        "tags": [te.text_content().strip() for te in tags_elements],
        "text": cleaned_text,
    }


def parse():
    """
    This function uses saved json files with raw posts data, parses it into json and saves into csv file.
    """
    Path(output_dir).mkdir(exist_ok=True)
    files = os.listdir(dir_name)
    ids = set()  # Save ids in set in order to not allow duplicates in output file
    res = []
    for file in tqdm(files):
        with open(os.path.join(dir_name, file), "r", encoding="utf-8") as f:
            content = f.read()
        articles_raw = json.loads(content)
        for a in articles_raw:
            parsed = parse_post(fromstring(a))
            if parsed and parsed["id"] not in ids:
                ids.add(parsed["id"])
                res.append(parsed)
    with open(os.path.join(output_dir, "parsed.csv"), "w", encoding="utf-8") as output:
        writer = DictWriter(output, fieldnames=res[0].keys())
        writer.writeheader()
        writer.writerows(res)


if __name__ == "__main__":
    parse()
