from datetime import timezone, datetime
from django.utils import timezone
from django.db import models

# 제품로그 테이블 
class product_log(models.Model):
    STATUS_CHOICES = (
        ('출고', '출고'),
        ('입고', '입고'),
    )


     # 자동 생성되는 ID 필드를 Primary Key로 설정
    id = models.AutoField(primary_key=True)



     # 외래 키 설정 (다대일 관계)
    user_id = models.ForeignKey(
        'mainApp.user_info',
        to_field='user_id',
        db_column='user_id',
        on_delete=models.CASCADE
    )

    productInfo_barcodeNum = models.ForeignKey(
        'scannerApp.product_info',
        to_field='barcode_num',
        db_column='productInfo_barcodeNum',
        on_delete=models.CASCADE
    )


    # 기타 필드
    change_quantity = models.IntegerField(null=True)
    date_time = models.DateTimeField(default=timezone.now)
    storage_retrieval = models.CharField(max_length=2, choices=STATUS_CHOICES)

    # 디버깅용, 인스턴스 생성하면 : product_log_entry = product_log(change_quantity=10, storage_retrieval="입고")
    # 출력 결과: "10 - 입고"
    def __str__(self):
        return f"{self.change_quantity} - {self.storage_retrieval}"
    