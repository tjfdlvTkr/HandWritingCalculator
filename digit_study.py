import cv2
import numpy as np

str_dic = { 0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5',
            6:'6', 7:'7', 8:'8', 9:'9', 10:'(', 11:')'}

def resize20(digitImg):
    img = cv2.imread(digitImg)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret = cv2.resize(gray, (20, 20), fx=1, fy=1, interpolation=cv2.INTER_AREA)

    ret, thr = cv2.threshold(ret, 127, 255, cv2.THRESH_BINARY_INV)

    cv2.imshow('ret', thr)

    return thr.reshape(-1, 400).astype(np.float32)

def learningDigit():
    img = cv2.imread('_data/digits.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 20 x 20
    digits_width = 2000
    digits_height = 1200

    cells = [np.hsplit(row, digits_width // 20) for row in np.vsplit(gray, digits_height // 20)]
    x = np.array(cells)

    train = x[:,:].reshape(-1, 400).astype(np.float32)

    # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, (, ), +, -, 나누기, %, =
    k = np.arange(12) #17
    train_labels = np.repeat(k, 500)[:, np.newaxis]

    np.savez('digits_for_ocr.npz', train=train, train_labels=train_labels)
    print('Data Saved')

def loadLearningDigit(ocrdata):
    with np.load(ocrdata) as f:
        traindata = f['train']
        traindata_labels = f['train_labels']

    return traindata, traindata_labels

def OCR_for_Digits(test, traindata, traindata_labels):
    knn = cv2.ml.KNearest_create()
    knn.train(traindata, cv2.ml.ROW_SAMPLE, traindata_labels)
    ret, result, neighbors, dist = knn.findNearest(test, k=5)

    return result

def detDigits(img, x, y, w, h):
    global str_dic

    img_cut = img[y:y+h, x:x+w]

    gray = cv2.cvtColor(img_cut, cv2.COLOR_BGR2GRAY)
    ret = cv2.resize(gray, (20, 20), fx=1, fy=1, interpolation=cv2.INTER_AREA)

    ret, thr = cv2.threshold(ret, 127, 255, cv2.THRESH_BINARY_INV)

    dig = thr.reshape(-1, 400).astype(np.float32)

    traindata, traindata_labels = loadLearningDigit('digits_for_ocr.npz')
    result = OCR_for_Digits(dig, traindata, traindata_labels)

    return str_dic[int(result[0][0])]

def main():
    global str_dic

    #learningDigit()
    ocrdata = 'digits_for_ocr.npz'
    traindata, traindata_labels = loadLearningDigit(ocrdata)
    digits = ['_testdata/' + str(x) + '.png' for x in range(12)]
    
    str_dic = { 0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5',
                6:'6', 7:'7', 8:'8', 9:'9', 10:'(', 11:')'}

    print(traindata.shape)
    print(traindata_labels.shape)

    savenpz = False
    for digit in digits:
        test = resize20(digit)
        result = OCR_for_Digits(test, traindata, traindata_labels)

        print(result)
        print(str_dic[int(result[0][0])])

        # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, (, ), +, -, 나누기, %, =
        # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, Q, W, E, R,     T, Y, U
        rec_dic = { 48:'0', 49:'1', 50:'2', 51:'3', 52:'4', 53:'5',
                    54:'6', 55:'7', 56:'8', 57:'9', 81:'10', 87:'11'}
                    #69:'12', 82:'13', 84:'14', 89:'15', 85:'16'}
                    
        k = cv2.waitKey(0) & 0xFF 
        if k in list(rec_dic.keys()):
            savenpz = True
            traindata = np.append(traindata, test, axis=0)
            new_label = np.array(int(rec_dic[k])).reshape(-1, 1)
            traindata_labels = np.append(traindata_labels, new_label, axis=0)

    cv2.destroyAllWindows()
    if savenpz:
        np.savez('digits_for_ocr.npz', train=traindata, train_labels=traindata_labels)

# - Training Start
#main()