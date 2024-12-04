from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
import cv2
import numpy as np
from .models import product_info
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
        
        barcode_lst = []
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
def save_barcodes_to_db(request, barcode_data_list):
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
                cursor.execute("SELECT COUNT(*) FROM scannerapp_product_info WHERE barcode_num = %s", (data[0],))
                cnt = cursor.fetchone()[0]

                if cnt == 0:
                    cursor.execute("INSERT INTO scannerapp_product_info (barcode_num, barcode_structure) VALUES (%s, %s)", (data[0], data[1]))
                    db.commit()
                else:
                    # 바코드가 이미 존재하는 경우 제품 정보 렌더링
                    return render_product_info(request, data[0])
            else:
                print(f"Invalid data format: {data}")

        db.commit()
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    finally:
        cursor.close()
        db.close()

    return render_product_info(request, data[0])

def render_product_info(request, barcode_num):
    try:
        db = connect_to_db()
        cursor = db.cursor()

        # 특정 바코드 번호로 데이터 조회
        cursor.execute("SELECT barcode_num, product_name, quantity, product_memo, barcode_structure FROM scannerapp_product_info WHERE barcode_num = %s", (barcode_num,))
        value = cursor.fetchone()

        if value:
            # 조회된 데이터를 딕셔너리로 변환
            product_info = {
                'barcode_num'     : value[0],
                'product_name'    : value[1],
                'quantity'        : value[2],
                'product_memo'    : value[3],
                'barcode_structure' : value[4]
            }
            context = {'product_info': product_info}
            return render(request, 'result.html', context)
        else:
            return render(request, 'result.html', {'error': 'Product not found'})
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        return render(request, 'result.html', {'error': 'Database error'})
    finally:
        cursor.close()
        db.close()

def scan_and_save_barcodes(request):
    cap = cv2.VideoCapture(0)
    recognized_barcodes = set()  # 중복 방지 셋 생성
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 바코드가 있으면 MySQL에 저장
            barcode_data_list = decode_barcode(frame)
            if barcode_data_list:
                for barcode_data in barcode_data_list:
                    if barcode_data not in recognized_barcodes:
                        recognized_barcodes.add(barcode_data)  # 중복 방지 셋에 저장
                        cap.release()
                        cv2.destroyAllWindows()
                        return save_barcodes_to_db(request, [barcode_data])
                        # HTML이 렌더링된 경우 응답 반환

                # 바코드가 인식된 후 처리되면 루프를 종료
                cap.release()
                cv2.destroyAllWindows()
                return HttpResponse("Barcode processed and saved.")
                
            cv2.imshow("Barcode Scanner", frame)

            # 'q' 키를 누르면 루프 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    # 바코드가 인식되지 않고 종료되었을 때 기본 응답 반환
    return HttpResponse("No barcode detected or operation canceled.")


def scan(request) :
    return render(request, 'scan.html')

def update_product(request):
    if request.method == 'POST':
        barcode_num = request.POST['barcode_num']
        product_name = request.POST.get('product_name', None)
        quantity = request.POST.get('quantity', None)
        product_memo = request.POST.get('product_memo', None)

        try:
            db = connect_to_db()
            cursor = db.cursor()

            # 데이터 업데이트 실행
            cursor.execute(
                """
                UPDATE scannerapp_product_info
                SET product_name = %s, quantity = %s, product_memo = %s
                WHERE barcode_num = %s
                """,
                (product_name, quantity, product_memo, barcode_num)
            )
            db.commit()
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
        finally:
            cursor.close()
            db.close()

        return render(request, 'success.html')
    return HttpResponse("Invalid request.")
