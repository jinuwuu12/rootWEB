from django.db import models

# models.Model 은 Django 내부의 데이터베이스 테이블과 상호작용을 위한 기본 클래스 상속
class barcode_info(models.Model):
    barcode_structr = models.CharField(max_length=100, default="EAN-13")
    barcode_num = models.CharField(max_length=100, default="0000000000000")
    
class Barcode_img(models.Model):
    image = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

# 메인 데이터베이스
class customer_info(models.Model):
    classification   = models.CharField(max_length=100, default='분류없음')
    product_name     = models.CharField(max_length=100, default='상품명없음')
    product_quantity = models.IntegerField(default=0)
    product_image    = models.BinaryField(null=True, blank=True)
    product_memo     = models.TextField(default='메모없음')
    
    def __str__(self):
        return f'{self.product_name} ({self.classification})'