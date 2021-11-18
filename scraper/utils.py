import logging
import sys
from typing import List
from lxml.html import fromstring, tostring

default_headers = {
    "authority": "pikabu.ru",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7,da;q=0.6",
    "cookie": "pcid=jYDleGx8vv2; sf=0; zukoVisitorId=YvEe9bnKqRxeJoW6qSv9DS94ATChNCna; _ym_uid=1614254812820875768; _ym_d=1614254812; _ga=GA1.2.517054697.1614254813; tmr_lvid=4065e0635307cc9e3cffabb261d4f554; tmr_lvidTS=1614546674099; tmr_reqNum=5; _gid=GA1.2.1428891017.1615125979; PHPSESS=6hol1gvfpuaanffasvdpadol4n; _ym_isad=1; fps=d0b49c942cdf5e18cbd7d82a83c5f6cd1a; is_scrollmode=1; ulfs=1615230745; pin_8064729=1; pkb_modern=11; k2s7=K-M:B:DEjC; la=1615231028_3948_4219_4219__; bs=F1; vn_buff=[8065360]; la=1615232056_3948_4219_4219__; pcid=jYDleGx8vv2; sf=0",
}


def get_logger(name):
    logger = logging.Logger(name)
    handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)
    return logger


def extract_articles(html: str) -> List[str]:
    """
    Extracts article tags which have data-author-id attribute. Articles without that tag are advertising posts which we
    are not interested in.
    :param html: content of html page as string
    :return: list of content of article tags as strings
    """
    tree = fromstring(html)
    articles = tree.xpath("//article[@data-author-id]")
    return [(tostring(a, encoding="unicode")) for a in articles]