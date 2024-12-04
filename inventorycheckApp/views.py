from django.shortcuts import render


# DB에서 조회하는 임포트
from django.shortcuts import render
from django.db import connection


# 조회된 내용 저장하는 임포트
import openpyxl
from django.http import HttpResponse
from django.db import connection


# 기간 선택 임포트
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # print('TEST')
    return render(request, 'IC_Main.html')
# Create your views here.



# userId + DB에서 조회
def index_with_userid_selected_date(request):
    user_id = request.GET.get('userId', None)  # GET 요청에서 'userId' 값을 가져옴
    selected_date = request.GET.get('selected_date', None)
    products = []
    # print("Received userId:", user_id)  # 터미널에 userId 출력

    if user_id:
        # Cursor를 사용해 userId 기반으로 데이터를 조회
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT barcode_num, barcode_structure, product_name, classification, quantity, product_img, product_memo
                FROM scannerapp_product_info
                WHERE user_id = %s
            """, [user_id])
            rows = cursor.fetchall()

        # 데이터 변환
        products = [
            {'barcode_num': row[0], 'barcode_structure': row[1], 'product_name': row[2], 'classification': row[3],
             'quantity': row[4], 'product_img': row[5], 'product_memo': row[6]} 
            for row in rows
        ]
        # products 내용을 콘솔에 출력하여 확인
        # print("Products fetched:", products)

    return render(request, 'IC_Main.html', {'products': products,'user_id': user_id})




# 조회 내용 엑셀 파일로 저장
def download_excel(request):
    # 엑셀 워크북 및 시트 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Product Data'

    # 데이터베이스에서 데이터를 조회
    user_id = request.GET.get('userId', None)
    print(user_id)

    # rows 초기화
    rows = []


    if user_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT barcode_num, barcode_structure, product_name, classification, quantity, product_img, product_memo
                FROM scannerapp_product_info
                WHERE userInfo_id = %s
            """, [user_id])
            rows = cursor.fetchall()

    # 엑셀 파일에 헤더 작성
    headers = ['바코드 번호', '바코드 구조', '상품명', '분류', '수량', '상품 사진', '메모']
    ws.append(headers)

    # 데이터 삽입
    for row in rows:
        ws.append(row)

    # 엑셀 파일을 HTTP 응답으로 반환
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_data.xlsx'
    
    # 엑셀 파일을 응답으로 전달
    wb.save(response)
    return response
