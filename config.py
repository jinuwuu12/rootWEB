# config.py

class Config:
    def __init__(self):
        # 데이터베이스 설정
        self.host = 'localhost'
        self.user = 'Park'
        self.password = 'park000721'
        self.database = 'new_schema'
        self.port = 3306

# config 인스턴스를 생성하여 사용할 수 있도록 함
config = Config()
