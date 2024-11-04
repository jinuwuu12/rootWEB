from django.apps import AppConfig


class ScannerappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scannerApp'

    def ready(self):
        import scannerApp.signals  # signals 파일을 임포트하여 등록

    