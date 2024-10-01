from django.db import models
from django.utils import timezone

# 바코드 정보 테이블 
# 모델을 새로정의하는 과정에서 오류가나서 barcode_info2로 변경한후 사용예정 필요없는 코드이나 마이그레이션 과정에서 오류로인해 지우지않음
class barcode_info(models.Model):
    barcode_structr = models.CharField(max_length=100, default="EAN-13", primary_key=True)
    barcode_num = models.CharField(max_length=100, unique=True, null=False) 

    def __str__(self):
        return self.barcode_num
    
# scannerApp database

# 유저 테이블
class user_info(models.Model):
    user_id = models.CharField(max_length=100, primary_key=True)
    user_password = user_password = models.CharField(max_length=128)
    user_email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15)
    sign_up_day = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user_id} ({self.user_name})'

# 제품정보 테이블
class product_info(models.Model):
    product_name   = models.CharField(max_length=100, primary_key=True)
    classification = models.CharField(max_length=100)
    quantity       = models.IntegerField()
    product_img    = models.BinaryField(null=True, blank=True)
    product_memo   = models.TextField(null=True, blank=True)
    product_count  = models.IntegerField()

# 제품로그 테이블 
class product_log(models.Model):
    
    STATUS_CHOICES = (
        ('출고', '출고'),
        ('입고', '입고'),
    )
    
    change_quantity = models.IntegerField()
    timestamp  = models.DateTimeField(default=timezone.now)
    storage_retrieval = models.CharField(max_length=2, choices=STATUS_CHOICES)
    
    def __str__(self):
        return f"{self.change_quantity} - {self.storage_retrieval}"
    
    