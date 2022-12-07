import requests
from bs4 import BeautifulSoup

mss_sub_categories = {
    "상의": "001006",
    "하의": "003002",
    "아우터": "002008"
    }
def get_category_id(mss_category_id, main_category):
    url = f"https://www.musinsa.com/categories/item/{mss_category_id}?d_cat_cd={mss_category_id}&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select("div#category_2depth_list>dl>dd>ul>li")
    for item in items:
        mapping = item.get("data-filter-value")
        name = item.get("data-filter-text").split(":")[1].strip()
        if "기타" not in name:
            print("==============")
            print(main_category, mapping, name, sep=" || ")

for main, id in mss_sub_categories.items():
    get_category_id(id, main)