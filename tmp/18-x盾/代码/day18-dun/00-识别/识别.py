import ddddocr

with open("front.png", mode='rb') as f:
    slice_bytes = f.read()

with open("bg.png", mode='rb') as f:
    bg_bytes = f.read()

slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
res = slide.slide_match(slice_bytes, bg_bytes, simple_target=True)
x1, y1, x2, y2 = res['target']
print(x1)
