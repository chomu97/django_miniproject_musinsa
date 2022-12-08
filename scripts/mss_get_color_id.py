import requests
from bs4 import BeautifulSoup
from closet.models import Color

def run():
    # mss_category_id = "002023" # 후리스
    mss_category_id = "001006" # 니트

    url = f"https://www.musinsa.com/categories/item/{mss_category_id}?d_cat_cd={mss_category_id}&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select("ul#toolTip>li")
    for item in items[:5]:
        mapping = item.select('a.color_list')[0].get("data-filter-value")
        name = item.select('a.color_list')[0].get('data-filter-text')
        
        if Color.objects.filter(name__iexact=name).count() == 0:
            data = {
                "mapping" : mapping,
                "name" : name,
            }
            Color(**data).save()
            print(name, "color saved")
    if Color.objects.filter(name__iexact="기타 색상").count() == 0:
        data = {
            "mapping" : "",
            "name" : "기타 색상"
        }
        Color(**data).save()
        print("기타 색상 color saved")