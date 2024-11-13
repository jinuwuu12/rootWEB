from django.db import models

# 제품정보 테이블(바코드 정보포함)
class product_info(models.Model):
    # 바코드 스캔을 통해 가져오는 부분
    barcode_num = models.CharField(max_length=100, default='0000000000000', unique=True, primary_key=True)  # 수퍼키

    # 사용자 입력 컬럼
    product_name = models.CharField(null=True, max_length=100)
    classification = models.CharField(null=True, max_length=100)
    initial_stock = models.IntegerField(null=True)  # 초기 재고
    current_quantity = models.IntegerField(null=True)  # 현재 수량

    # 이미지 파일 경로 저장
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)

    # 기타 필드
    product_memo = models.TextField(null=True, blank=True)
    barcode_structure = models.CharField(max_length=100, default="EAN-13")

    #외래키 설정
    user_id = models.ForeignKey(
        'mainApp.user_info',
        to_field='user_id',
        on_delete=models.CASCADE,
        db_column='user_id'
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barcode_num', 'user_id'], name='superkey_productInfo')
        ]

    def __str__(self):
        return f"{self.barcode_num} - {self.barcode_structure}"
