import requests
from bs4 import BeautifulSoup
from closet.models import Clothes, Category, Color

def run():
    def get_like_count(url): # javascript 문제로 사용하지 않음.
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


    def save_data(category_object: Category, color_object: Color):
        # mss_category_id = "002023" # 후리스
        mss_category_id = category_object.mapping # 니트
        color = color_object.mapping
        url = f"https://www.musinsa.com/categories/item/{mss_category_id}?d_cat_cd={mss_category_id}&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&kids=&color={color}&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="
        res = requests.get(url)

        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.select("ul#searchList>li.li_box")


        # 내일 Color별로, Category 별로 request 돌면서 DB에 저장되는지 확인 필요.
        # 아래에 조건문으로 중복된 아이템 들어가지 않도록 처리 필요. item_url으로 검사할듯
        for item in items:
            thumbnail = "https:" + item.select("img.lazyload")[0].get("data-original")
            name = item.select("a.img-block")[0].get("title").strip()
            brand = item.select("p.item_title>a")[0].text.strip()
            original_price = item.select("p.price")[0].text.split()
            selling_price = str(0) if len(original_price) == 1 else original_price[1]
            original_price = original_price[0]
            original_price = won2int(original_price)
            selling_price = won2int(selling_price)
            if selling_price == 0:
                selling_price = original_price
            if item.find('span','bar') != None:
                star_rate = int(item.select("span.bar")[0].get("style").split(":")[1][:-1])
                review_cnt = won2int(item.select("span.count")[0].text)
            else:
                star_rate = 0
                review_cnt = 0
            item_url = "https:"+item.select("a.img-block")[0].get("href")
            if Clothes.objects.filter(url__iexact=item_url).count() == 0:
                data = {
                    "name": name,
                    "brand": brand,
                    "originalPrice": original_price,
                    "sellingPrice": selling_price,
                    "reviewCount": review_cnt,
                    "starRate": star_rate,
                    "thumbnailUrl": thumbnail,
                    "url": item_url,
                    "categoryId": Category.objects.get(mapping=category_object.mapping),
                    "colorId": Color.objects.get(mapping=color_object.mapping),
                }
                Clothes(**data).save()
                print("==============")
                print(name, " saved")


    categories = Category.objects.all()
    colors = Color.objects.all()

    for category_object in categories:
        for color_object in colors:
            save_data(category_object, color_object)