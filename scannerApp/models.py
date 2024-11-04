from django.db import models


# 제품정보 테이블(바코드 정보포함) --> 뷰 로직 수정 필요함(20241005 변경)
class product_info(models.Model):
    # 바코드 스캔을 통해 가져오는 부분
    barcode_num = models.CharField(max_length=100, default='0000000000000', unique=True, primary_key=True) #수퍼키
    # 사용자 입력 컬럼
    product_name   = models.CharField(null = True, max_length=100)
    classification = models.CharField(null = True, max_length=100)
    quantity       = models.IntegerField(null = True)
    product_img    = models.BinaryField(null=True, blank=True)
    product_memo   = models.TextField(null=True, blank=True)
    product_count  = models.IntegerField(null = True)
    # 바코드 형식 ex) EAN-13
    barcode_structure = models.CharField(null = True, max_length=100, default="EAN-13")
    
     # 외래키 설정 (다대일 관계)
    userInfo_id = models.ForeignKey(
        'mainApp.user_info', 
        null = True, 
        to_field='user_id', 
        default='유저아이디', 
        on_delete=models.CASCADE,
        db_column='userInfo_id'
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['barcode_num', 'userInfo_id'], name='superkey_productInfo')
        ]
        
    def __str__(self):
        return f"{self.barcode_num} - {self.barcode_structr}"


    
    