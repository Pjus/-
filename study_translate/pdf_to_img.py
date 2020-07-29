from pdf2image import convert_from_path

def pdfToimg(pdfpath, savepath):
    pages = convert_from_path(pdfpath)

    for idx, img in enumerate(pages):
        img.save(savepath + str(idx).zfill(len(str(len(pages)))) + '.jpg', 'JPEG') # pdf_넘버링.jpg 이런 방식으로 네이밍을 합니다.
