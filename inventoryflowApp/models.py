from datetime import timezone, datetime
from django.utils import timezone
from django.db import models

# 제품로그 테이블 
class product_log(models.Model):
    STATUS_CHOICES = (
        ('출고', '출고'),
        ('입고', '입고'),
    )
    change_quantity = models.IntegerField(null = True)
    date_time  = models.DateTimeField(default=timezone.now, unique=True) #수퍼키
    storage_retrieval = models.CharField(max_length=2, choices=STATUS_CHOICES, primary_key=True)
    
    #외래키 설정
    userInfo_id = models.OneToOneField('mainApp.user_info', 
                                       to_field='user_id', 
                                       default='유저아이디',
                                       db_column='userInfo_id',
                                       on_delete=models.CASCADE ) #수퍼키
    
    productInfo_barcodeNum = models.OneToOneField('scannerApp.product_info',
                                                  to_field='barcode_num',
                                                  db_column='productInfo_barcodeNum',
                                                  on_delete=models.CASCADE) #수퍼키
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date_time', 'userInfo_id','productInfo_barcodeNum'], name='superkey_productLog')
        ]
        
    def __str__(self):
        return f"{self.change_quantity} - {self.storage_retrieval}"
    