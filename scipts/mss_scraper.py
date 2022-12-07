import requests
from bs4 import BeautifulSoup

# mss_category_id = "002023" # 후리스
mss_category_id = "001006" # 니트
color = ""
url = f"https://www.musinsa.com/categories/item/{mss_category_id}?d_cat_cd={mss_category_id}&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color={color}&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="

def get_like_count(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    like_res = requests.get(url, headers=header)
    soup = BeautifulSoup(like_res.text, 'html.parser')
    like_count = soup.select("span.prd_like_cnt")[0]
    return like_count


def won2int(won):
    result = ""
    for i in won:
        if i.isdigit():
            result+=i
    return int(result)

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
items = soup.select("ul#searchList>li.li_box")

for item in items:
    thumbnail = "https:" + item.select("img.lazyload")[0].get("data-original")
    name = item.select("a.img-block")[0].get("title")
    brand = item.select("p.item_title>a")[0].text
    original_price = item.select("p.price")[0].text.split()
    selling_price = str(0) if len(original_price) == 1 else original_price[1]
    original_price = original_price[0]
    selling_price = won2int(selling_price)
    original_price = won2int(original_price)
    star_rate = int(item.select("span.bar")[0].get("style").split(":")[1][:-1])
    review_cnt = item.select("span.count")[0].text
    item_url = "https:"+item.select("a.img-block")[0].get("href")
    print("=====================")
    print(thumbnail, name, brand, original_price, selling_price, star_rate, review_cnt, item_url, sep="\n")
