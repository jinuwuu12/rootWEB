# scannerApp/signals.py
# scannerApp에 데이터 추가할 시 현재 시각과 userId도 inventoryflowapp_product_log 테이블로 저장되도록


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import product_info
from inventoryflowApp.models import product_log

@receiver(post_save, sender=product_info)
def create_product_log(sender, instance, created, **kwargs):
    if created:  # 새로운 데이터가 생성될 때만 실행
        product_log.objects.create(
            change_quantity=instance.quantity,  # 예시: 초기 수량을 변경 수량으로
            date_time=timezone.now(),  # 현재 시각을 설정
            storage_retrieval='입고',  # 기본 상태를 '입고'로 설정
            userInfo_id=instance.userInfo_id,  # product_info의 userInfo_id 값 사용
            productInfo_barcodeNum=instance  # 외래키로 product_info 인스턴스 할당
        )
