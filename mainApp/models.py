from django.db import models

# 유저 테이블
class user_info(models.Model):
    user_id = models.CharField(max_length=100, null=False, unique=True, primary_key=True)
    user_password = user_password = models.CharField(max_length=128)
    user_email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15)
    sign_up_day = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'user_email'], name='superkey_userinfo')
        ]
    
    def __str__(self):
        return f'{self.user_id} ({self.user_name})'