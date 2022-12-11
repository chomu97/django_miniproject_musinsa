from django.shortcuts import render
from .models import Clothes, Category, Color
import random

# Create your views here.
def home(request):
    rand_idx = set()
    max_idx = Clothes.objects.count()
    while len(rand_idx) != 20:
        rand_idx.add(random.randint(1,max_idx))
    data = Clothes.objects.filter(id__in=rand_idx).order_by('-reviewCount')
    discount = []
    for d in data:
        discountRate= int((1 - d.sellingPrice/d.originalPrice) * 100)
        discount.append(discountRate)
    return render(request, 'main.html', {"data":zip(data, discount),})

def show_dashboard(request):
    if request.method == "POST":
        selected_main_category = request.POST.get('selected_main_category')
        selected_color = request.POST.get('selected_color')
        selected_category = request.POST.get('selected_category')
        # all query 기능 구현 필요.
        if "모든" in selected_main_category or "선택" in selected_main_category:
            selected_main_category = Category.objects.all().values_list('mainCategory').distinct()
        else:
            selected_main_category = Category.objects.filter(mainCategory__iexact=selected_main_category).values_list('mainCategory').distinct()
        if "모든" in selected_category or "선택" in selected_category:
            selected_category = Category.objects.all().values_list('name').distinct()
        else:
            selected_category = Category.objects.filter(name__iexact=selected_category).values_list('name').distinct()
        if "모든" in selected_color or "선택" in selected_color:
            selected_color = Color.objects.all().values_list('name').distinct()
        else:
            selected_color = Color.objects.filter(name__iexact=selected_color).values_list('name').distinct()
        
        categoryFilter = Category.objects\
            .filter(mainCategory__in=selected_main_category)\
                .filter(name__in=selected_category).values_list('id')
        colorFilter = Color.objects.filter(name__in=selected_color).values_list('id')
        filter_option = {
            "categoryId__in":categoryFilter,
            "colorId__in":colorFilter
        }   
        clothes = Clothes.objects.filter(**filter_option).order_by('-reviewCount')[:5]
    else:
        clothes = Clothes.objects.all().order_by("-reviewCount")[:5]
    categories = Category.objects.all()
    colors = Color.objects.all()
    main_categories = Category.objects.all().values_list('mainCategory').distinct()
    selling_order = rank_index([c.sellingPrice for c in clothes], False)
    discount = []
    for c in clothes:
        discountRate= int((1 - c.sellingPrice/c.originalPrice) * 100)
        discount.append(discountRate)
    discount_order = rank_index(discount, True)
    star_order = rank_index([c.starRate for c in clothes], True)
    review_order = rank_index([c.reviewCount for c in clothes], True)
    order_list = list(zip(selling_order, discount_order, star_order, review_order))
    backgroundColor = ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(45, 183, 87, 0.2)','rgba(255, 193, 7, 0.2)','rgba(153, 102, 255,0.2)']
    borderColor = ['rgb(255, 99, 132)','rgb(54, 162, 235)','rgb(45, 183, 87)','rgb(255, 193, 7)','rgb(153, 102, 255)']
    data ={
        "clothes_chart":zip(clothes,order_list,backgroundColor,borderColor),
        "categories":categories,
        "colors":colors,
        "main_categories":main_categories,
        "clothes":zip(clothes, ["#ff638433","#36a2eb33","#2db75733","#ffc10733","#9966ff33"]),
    }
    return render(request, 'closet/dashboard.html', data)


def rank_index(lst: list, reverse: bool):
    order_lst = []
    for i in lst:
        order_lst.append(i)
    order_lst.sort(reverse=reverse)
    result = []
    for v in lst:
        result.append(order_lst.index(v)+1)
    return result