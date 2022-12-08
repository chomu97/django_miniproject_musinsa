from django.db import models

# Create your models here.
class Category(models.Model):
    mainCategory = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    mapping = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Category"
        
    def __str__(self):
        return f"{self.pk} || {self.mainCategory} || {self.name} || {self.mapping}"

class Color(models.Model):
    name = models.CharField(max_length=50)
    mapping = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Color"
    
    def __str__(self):
        return f"{self.pk} || {self.name} || {self.mapping}"


class Clothes(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    originalPrice = models.IntegerField()
    sellingPrice = models.IntegerField()
    reviewCount = models.IntegerField(default=0)
    starRate = models.IntegerField(default=0)
    thumbnailUrl = models.CharField(max_length=200)
    url = models.CharField(max_length=100, default="")
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE,)
    colorId = models.ForeignKey(Color, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Clothes"
    
    def __str__(self):
        return f"{self.categoryId.name} || {self.colorId.name} || {self.name} || {self.brand}"