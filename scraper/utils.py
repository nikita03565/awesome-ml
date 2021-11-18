import logging
import sys
from typing import List
from lxml.html import fromstring, tostring

default_headers = {
    "authority": "pikabu.ru",
    "cache-control": "max-age=0",
    "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "dnt": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-language": "en-GB,en;q=0.9",
    "cookie": "PHPSESS=8ebfqvk63ob4mse3h9m0la531v; is_scrollmode=1; pcid=jRUlRUGbsv2; grex2=%7B%22sidebar_adv_20210714%22%3A%22gr1%22%7D; la=1637245206_10334__10334__; clpr1=Aw.AA.AAA.AAAAAAAAAAA; pkb_modern=11; zukoVisitorId=UW4oIamRtVTDyfPX0eQTC8PxtwdeHn9y; bs=E0; _ym_uid=163724520823638306; _ym_d=1637245208; _ga=GA1.2.942804580.1637245208; _gid=GA1.2.803218438.1637245208; _gat_gtag_UA_28292940_1=1; _ym_isad=2; _fbp=fb.1.1637245208333.1684597788; ulfs=1637245208; sf=0; cto_bundle=54Voe19aTnJNU2I3VnZuVWVkOTFzaXNXSSUyRnZ2V0FUUENjdHdQUDUzMjFtbXYxQ25DQ3lsY0lKVTJMb1JDV050YzY5Y01mWllHSG52Y3F1aHNPTlExMWpiTyUyRnQlMkZZJTJCZDVzSXBKYk5OMHY2JTJCYlhwR1ZaS01EOVliTjNmWFdNMkZvak93MnlFcEVtYk9sUm12NmZIRjBLNGlFRnNnJTNEJTNE; __gads=ID=eebb38a1773e228d:T=1637245208:S=ALNI_MZfOa6a4on7reERkIVXeoTnoVrClg; vn_buff=[8624411]; grex2=%7B%22sidebar_adv_20210714%22%3A%22gr1%22%7D; la=1637245206_10334__10334__; pcid=jGMlmZXQtv2; sf=0; ulfs=1637245244",
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
