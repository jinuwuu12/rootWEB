from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
import cv2
import numpy as np

# 바코드 스캔 함수

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
        
        barcode_lst = []
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
    