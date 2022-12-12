import cv2
import digit_study as distu

def detFormula(fname):
    img = cv2.imread(fname)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, rect_kernel)
    dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    im2 = img.copy()
    width = 20

    ocrdata = 'ocr_model.npz'
    traindata, traindata_labels = distu.loadModel(ocrdata)

    digit_list = []

    for c in contours:
        [x, y, w, h] = cv2.boundingRect(c)

        if h < w // 2: # -
            h += 30
            y -= 15
         
        digit_list.append([x, y, w, h])


    for i in range(len(digit_list) - 1):
        min = i
        for j in range(i+1, len(digit_list)):
            mx, my, mw, mh = digit_list[min]
            jx, jy, jw, jh = digit_list[j]

            if (jy+jh < my):
                min = j
            elif (jx < mx) and ((my in range(jy, jy+jh+1)) or (my+mh in range(jy, jy+jh+1)) or (jy in range(my, my+mh+1)) or (jy+jh in range(my, my+mh+1))):
                min = j
        
        digit_list[min], digit_list[i] = digit_list[i], digit_list[min]

    string = ""

    for x, y, w, h in digit_list:
        if w > 15 and h > 15 and w < 300 and h < 300:
            cropped = im2[y:y + h, x:x + w]
            cropped = cv2.resize(cropped, (width - 6, width - 6), fx=1, fy=1, interpolation=cv2.INTER_AREA)

            gray_c = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            thresh_c = cv2.threshold(gray_c, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)[1]
            kernel_c = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
            thresh_c = cv2.morphologyEx(thresh_c, cv2.MORPH_OPEN, kernel_c)

            base = cv2.imread('base.png', cv2.COLOR_BGR2GRAY)
            base = cv2.resize(base, (width, width), fx=1, fy=1, interpolation=cv2.INTER_AREA)
            base = 255 - base
            hc, wc = cropped.shape[:2]

            crop_done = base[3:hc+3,3:wc+3]
            cv2.copyTo(cropped, thresh_c, crop_done)

            cutimg = distu.resizeImg(base, width)

            result = distu.ocrchar(cutimg, base, traindata, traindata_labels)
            string += str(result)

            rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 1)

    cv2.imwrite('_log/recg.png', im2)
    return string


#print(detFormula('_log/capture.png'))