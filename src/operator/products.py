import re
import requests
from bs4 import BeautifulSoup


def get_product_url(product: str) -> str:
    urls = get_product_urls(product)
    if urls:
        return urls[0]
    return ""

def get_product_urls(product: str) -> list[str]:
    q_product = [word.strip() for word in product.split(" ") if word.strip()]
    q_product = "+".join(q_product)
    url = f"https://www.google.com/search?q={q_product}&tbm=shop"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # These may change over time
    PRODUCT_CLASSES = ["KZmu8e", "i0X6df"]
    
    
    divs = []
    for class_value in PRODUCT_CLASSES:
        divs += soup.find_all("div", {"class": class_value})
    divs = list(map(str, divs))

    product_links = []
    for div in divs:
        anchors = BeautifulSoup(div, 'html.parser').find_all("a")
        anchors = list(map(str, anchors))
        if anchors:
            anchor = anchors[0]
            idx = anchor.find("href=")
            if idx != -1:
                idx += len("href=") + 1
                anchor = anchor[idx:]
                idx2 = anchor.find('"')
                href = anchor[:idx2]
                product_link = re.sub("&amp;", "&", href)
                product_links.append(product_link)

    return product_links
