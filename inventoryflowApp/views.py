from django.shortcuts import render
from django.db import connection
from datetime import datetime


# 기간 선택 임포트
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'IF_Main.html')






def IF_Main_selected(request):
    user_id = request.GET.get('userId')  # GET 요청에서 'userId' 값을 가져옴
    date_range = request.GET.get('selected_date_range')  # GET 요청에서 'selected_date_range' 값을 가져옴
    storage_retrieval = request.GET.get('storage_retrieval', '모두')  # 기본값은 "모두"
    logs = []

    if not user_id or not date_range:
        return render(request, 'error.html', {'error': 'User ID와 기간을 모두 입력해야 합니다.'})

    try:
        # "YYYY-MM-DD - YYYY-MM-DD" 형식으로 들어오는 날짜 범위를 분리
        start_date, end_date = date_range.split(' - ')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # SQL 쿼리 작성
        query = """
            SELECT id, change_quantity, date_time, storage_retrieval, productInfo_barcodeNum
            FROM inventoryflowApp_product_log
            WHERE user_id = %s AND date_time BETWEEN %s AND %s
        """
        params = [user_id, start_date, end_date]

        # "입고" 또는 "출고" 조건 추가
        if storage_retrieval != "모두":
            query += " AND storage_retrieval = %s"
            params.append(storage_retrieval)

        # Cursor를 사용해 데이터를 조회
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

        if rows:
            logs = [
                {
                    'id': row[0],
                    'change_quantity': row[1],
                    'date_time': row[2].strftime('%Y-%m-%d %H:%M:%S'),
                    'storage_retrieval': row[3],
                    'productInfo_barcodeNum': row[4]
                }
                for row in rows
            ]
    except Exception as e:
        return render(request, 'error.html', {'error': f'오류가 발생했습니다: {str(e)}'})

    return render(request, 'IF_Main.html', {'logs': logs, 'user_id': user_id, 'storage_retrieval': storage_retrieval})
