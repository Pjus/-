from pdf2image import convert_from_path

pages = convert_from_path('C:\\Users\\sundooedu\\Desktop\\DART_Crawling\\reference\\Machine Learning-Based Financial Statement Analysis.pdf')

for idx, img in enumerate(pages):
    img.save('./pdf_' + str(idx).zfill(len(str(len(pages)))) + '.jpg', 'JPEG') # pdf_넘버링.jpg 이런 방식으로 네이밍을 합니다.
