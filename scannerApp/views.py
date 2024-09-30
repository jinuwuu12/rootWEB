from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
import cv2
import numpy as np
from .models import Barcode_img, barcode_info
from config import config 
import mysql.connector    #DB 연결 (def connect_to_db)

# 이미지에서 바코드를 스캔하는 함수 - 이미지를 업로드했을 때 상품을 등록하기 위한 코드

# Config값
host     = config.host
user     = config.user
password = config.password
database = config.database
port     = config.port

barcode_lst = []
def barcode_reading_view(request):
    barcode_lst = []  # 함수 내에서 리스트 초기화
    if request.method == "POST" and request.FILES.get('barcode_image'):
        barcode_image = request.FILES['barcode_image']
        
        # 파일을 메모리에서 numpy 배열로 변환
        img_array = np.asarray(bytearray(barcode_image.read()), dtype=np.uint8)
        
        # 이미지를 컬러로 읽기
        barcode_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        # 이미지를 흑백으로 변환
        gray = cv2.cvtColor(barcode_img, cv2.COLOR_BGR2GRAY)
        
        # 바코드 디코딩 
        decoded = pyzbar.decode(gray)
        
        for d in decoded:
            barcode_data = d.data.decode('utf-8')
            barcode_lst.append(barcode_data)
            
            # 바코드 정보 출력 (디버깅용)
            print(f"Found barcode: {barcode_data}")

        # 바코드가 인식되었으면 DB에 저장
        if barcode_lst:
            # DB에 바코드 저장
            save_barcodes_to_db([(barcode_data, 'QR_CODE') for barcode_data in barcode_lst])
            return HttpResponse(f"바코드 내용: {', '.join(barcode_lst)}")
        else:
            return HttpResponse("바코드를 인식하지 못했습니다.")
    
    return render(request, 'scan_result.html')

def upload_page_view(request):
    return render(request, 'upload.html')

# mysql 데이터베이스 연결 설정 함수
def connect_to_db():
    return mysql.connector.connect(
        host=host,  # MySQL 호스트 주소
        user=user,  # MySQL 사용자명
        password=password,  # MySQL 비밀번호
        database=database,  # 사용할 데이터베이스
        port=port
    )


# 바코드 디코딩 함수(DB저장용)
def decode_barcode(frame):
    barcodes = pyzbar.decode(frame)
    barcode_data_list = []
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"Found {barcode_type} barcode: {barcode_data}")
        
        barcode_data_list.append((barcode_data, barcode_type))
    
    return barcode_data_list

# mysql 데이터베이스 연결 설정 함수
def connect_to_db():
    
    db_config = {
        'host': config.host,
        'user': config.user,
        'password': config.password,
        'database': config.database,
        'port': config.port
    }

    # MySQL에 연결
    return mysql.connector.connect(**db_config)


# 바코드를 MySQL에 저장하는 함수
def save_barcodes_to_db(barcode_data_list):
    try:
        print(">>>>>>> save_barcodes_to_db 함수 실행")
        db = connect_to_db()
        cursor = db.cursor()
        
        for data in barcode_data_list:
            # 데이터가 ndarray인지 확인하고, 튜플로 변환
            if isinstance(data, np.ndarray):
                data = tuple(data)  # ndarray를 튜플로 변환
            
            # 튜플인지 확인하고 길이가 2인 경우만 처리
            if isinstance(data, tuple) and len(data) == 2:
                cursor.execute("SELECT COUNT(*) FROM scannerapp_barcode_info WHERE barcode_structr = %s AND barcode_num = %s", (data[0], data[1]))
                cnt = cursor.fetchone()[0]

                if cnt == 0 :
                    cursor.execute("INSERT INTO scannerapp_barcode_info (barcode_structr, barcode_num) VALUES (%s, %s)", (data[0], data[1]))
                else :
                    print("나중에 바코드 중복될 때 사용할 부분")
            else:
                print(f"Invalid data format: {data}")
        
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    
# DB에 바코드 정보가 있는지 확인하는 함수
def is_barcode_exists(barcode):
    db = connect_to_db()
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM barcodes WHERE barcode = %s"
    cursor.execute(query, (barcode,))
    count = cursor.fetchone()[0]
    return count > 0

# DB안에 바코드 정보가 있는 경우 
def if_there_are_barcode_in_db(barcode_data_list):
    for barcode in barcode_data_list:
        # 데이터베이스에 바코드가 이미 존재하는지 확인
        if not is_barcode_exists(barcode):
            save_barcodes_to_db(barcode)
    

#카메라에서 실시간으로 바코드를 인식하고 MySQL에 저장

def scan_and_save_barcodes():
    cap = cv2.VideoCapture(0)
    recognized_barcodes = set() # 중복 방지 셋 생성
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            
            # 바코드가 있으면 MySQL에 저장
            barcode_data_list = decode_barcode(frame)
            if barcode_data_list:
                for barcode_data in barcode_data_list :
                    if barcode_data not in recognized_barcodes :
                        save_barcodes_to_db([barcode_data])
                        recognized_barcodes.add(barcode_data) #중복방지 셋에 저장
                        cap.release()
                        cv2.destroyAllWindows()
                        return
            cv2.imshow("Barcode Scanner", frame)
            #if ret == True:
                #break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


scan_and_save_barcodes()

