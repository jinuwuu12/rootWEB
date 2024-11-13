from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import product_info
from inventoryflowApp.models import product_log

@receiver(post_save, sender=product_info)
def create_product_log(sender, instance, created, **kwargs):
    # 새로운 데이터가 생성된 경우 (입고 케이스 1)
    if created:
        product_log.objects.create(
            change_quantity=instance.initial_stock,
            date_time=timezone.now(),
            storage_retrieval='입고',
            user_id=instance.user_id,
            productInfo_barcodeNum=instance
        )
    else:
        # 기존 데이터일 경우 현재 수량과 과거 수량을 비교하여 입고/출고 여부 결정

        # 이전 값 가져오기
        try:
            # 가장 최근의 로그에서 `change_quantity` 값 사용
            last_log = product_log.objects.filter(
                productInfo_barcodeNum=instance
            ).latest('date_time')
            previous_qty = last_log.change_quantity
        except product_log.DoesNotExist:
            # 로그가 없으면 `initial_stock` 값을 이전 값으로 사용
            previous_qty = instance.initial_stock

        # 현재 수량
        current_qty = instance.current_quantity

        # current_quantity가 증가한 경우 (입고)
        if current_qty > previous_qty:
            change_qty = current_qty - previous_qty
            storage_status = '입고'
        # current_quantity가 감소한 경우 (출고)
        elif current_qty < previous_qty:
            change_qty = previous_qty - current_qty
            storage_status = '출고'
        else:
            # 수량이 변경되지 않은 경우 로그를 기록하지 않음
            return

        # 입고 또는 출고 로그 생성
        product_log.objects.create(
            change_quantity=change_qty,
            date_time=timezone.now(),
            storage_retrieval=storage_status,
            user_id=instance.user_id,
            productInfo_barcodeNum=instance
        )
