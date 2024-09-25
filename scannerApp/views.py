from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
import cv2
import numpy as np
from .models import Barcode_img, barcode_info
import mysql.connector

# 바코드 스캔 함수

barcode_lst = []
def barcode_reading_view(request):
    if request.method == "POST" and request.FILES.get('barcode_image'):
        # 업로드된 파일 가져오기
        barcode_image = request.FILES['barcode_image']
        
        # 파일을 메모리에서 numpy 배열로 변환(변환해야 openCV에서 처리가능)
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

            # 바코드 영역에 사각형 그리기
            cv2.rectangle(barcode_img, 
                          (d.rect[0], d.rect[1]), 
                          (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), 
                          (0, 0, 255), 2)
            
        if barcode_lst:
            return HttpResponse(f"바코드 내용: {', '.join(barcode_lst)}")
        else:
            return HttpResponse("바코드를 인식하지 못했습니다.")
    
    return render(request, 'scan_result.html')

def upload_page_view(request):
    return render(request, 'upload.html')

# mysql 데이터베이스 연결 설정 함수
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",  # MySQL 호스트 주소
        user="root",  # MySQL 사용자명
        password="jinwoo123@",  # MySQL 비밀번호
        database="scanner_db",  # 사용할 데이터베이스
        port=3307
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

# 바코드를 MySQL에 저장하는 함수
def save_barcodes_to_db(barcode_data_list):
    db = connect_to_db()
    cursor = db.cursor()
    
    for data in barcode_data_list:
        # 데이터가 ndarray인지 확인하고, 튜플로 변환
        if isinstance(data, np.ndarray):
            data = tuple(data)  # ndarray를 튜플로 변환
        
        # 튜플인지 확인하고 길이가 2인 경우만 처리
        if isinstance(data, tuple) and len(data) == 2:
            cursor.execute("INSERT INTO scannerapp_barcode_info (barcode_structr, barcode_num) VALUES (%s, %s)", (data[0], data[1]))
        else:
            print(f"Invalid data format: {data}")
    
    db.commit()
    cursor.close()
    db.close()
    
    
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



########################################################################################################################
# 위함수에 대한 테스트 코드
def scan_and_save_barcodes_test():
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            barcode_data_list = decode_barcode(frame)
            
            # 바코드가 있으면 MySQL에 저장
            if is_barcode_exists(frame) > 0:
                save_barcodes_to_db(barcode_data_list)
                
            cv2.imshow("Barcode Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
scan_and_save_barcodes_test()


# 타입테스트를 위한 코드
# cap2 = cv2.VideoCapture(0)
# try:
#     while True:
#         ret2, frame2 = cap2.read()
#         print(frame2)
        
#         if not ret2:
#             break
        
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
            
#         cv2.imshow("Barcode Scanner", frame2)
        
# finally:
#     print(type(frame2))
#     cap2.release()
#     cv2.destroyAllWindows()
########################################################################################################################      

