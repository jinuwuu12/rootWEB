from django.shortcuts import render
import pyzbar.pyzbar as pyzbar
import cv2

# print(dir(cv2))
# help(cv2)

# 이미지를 읽고 배열로 변환하는 코드
# img = cv2.imread('C:/Users/admin/Desktop/rootWEB/scannerApp/img/cute_dog.jpg', cv2.IMREAD_COLOR)

# 배열로 변환한코드를 다시 이미지로 변환하는 코드
# cv2.imwrite('output.png', img)


# 이 아래로는 바코드에 대한 정보를 받아오는 코드임 
barcode_test_img = cv2.imread('scannerApp/img/barcode_test_img.jpg', cv2.IMREAD_COLOR)

# 흑백으로 바꿔주는 코드 
gray = cv2.cvtColor(barcode_test_img, cv2.COLOR_BGR2GRAY)

decoded = pyzbar.decode(gray)

barcode_lst = []
for d in decoded:
    print(d.data.decode('utf-8'))
    print(d.type)
    barcode_lst.append(d.data.decode('utf-8'))
    cv2.rectangle(barcode_test_img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (0, 0, 255), 2)

print(barcode_lst)