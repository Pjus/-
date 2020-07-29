import pytesseract
import os
import time


# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
# print(pytesseract.image_to_string('./pdf_img/pdf_00.jpg'))



def extractImg(imgs):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    for img in imgs:
        print(img)
        print(pytesseract.image_to_string('./pdf_img/' + img))
        study = pytesseract.image_to_string('./pdf_img/' + img)
        text = open('./txt/output.txt','a', encoding='utf-8')
        text.write(study)


if __name__ == "__main__":
    start = time.time()  # 시작 시간 저장

    
    path = "./pdf_img"
    file_list = os.listdir(path)

    # print ("file_list: {}".format(file_list))
    extractImg(file_list)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간