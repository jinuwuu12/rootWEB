from django.db import models

# models.Model 은 Django 내부의 데이터베이스 테이블과 상호작용을 위한 기본 클래스 상속
class barcode_info(models.Model):
    barcode_num = models.IntegerField()

