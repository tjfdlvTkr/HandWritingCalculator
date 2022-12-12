import cv2
import numpy as np

str_dic = {
    0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6',
    7:'7', 8:'8', 9:'9', 10:'+', 11:'-', 12:'*', 13:'/',
    14:'%', 15:'(', 16:')'
}

def learningDigit(char_num, ocrdata, width):
    image = cv2.imread('_data/digits.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    px = 8000
    py = 4000

    cells = [np.hsplit(row, px // width) for row in np.vsplit(gray, py // width)]
    x = np.array(cells)

    train = x[:,:].reshape(-1, width ** 2).astype(np.float32)

    k = np.arange(char_num)
    train_labels = np.repeat(k, 500)[:, np.newaxis]

    np.savez(ocrdata, train=train, train_labels=train_labels)

def loadModel(ocrdata):
    with np.load(ocrdata) as f:
        traindata = f['train']
        traindata_labels = f['train_labels']

    return traindata, traindata_labels

def resizeImg(test_img, width):
    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    ret = cv2.resize(gray, (width, width), fx=1, fy=1, interpolation=cv2.INTER_AREA)

    ret, thr = cv2.threshold(ret, 127, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('ret',thr)
    return thr.reshape(-1, width ** 2).astype(np.float32)

def ocrchar(img, traindata, traindata_labels):
    global str_dic

    knn = cv2.ml.KNearest_create()
    knn.train(traindata, cv2.ml.ROW_SAMPLE, traindata_labels)
    ret, result, neighbors, dist = knn.findNearest(img, k=5)
    print(ret, result, neighbors, dist)
    
    return str_dic[int(result[0][0])]

def imglearn(test_img_rs, k, traindata, traindata_labels):
    traindata = np.append(traindata, test_img_rs, axis=0)
    new_label = np.array(int(chr(k))).reshape(-1,1)
    traindata_labels = np.append(traindata_labels, new_label, axis=0)
    return traindata, traindata_labels

def main():
    global Mode

    testdata_num = 10

    char_num = 10
    
    ocrdata = 'ocr_model.npz'
    width = 80

    if Mode == 1: learningDigit(char_num, ocrdata, width)

    testchar = ['_testdata/' + str(x) + '.png' for x in range(testdata_num)]

    savevar = False
    traindata, traindata_labels = loadModel(ocrdata)
    for char in testchar:
        test_img = cv2.imread(char)
        test_img_rs = resizeImg(test_img, width)
        result = ocrchar(test_img_rs, traindata, traindata_labels)

        #print('Result :', int(result[0][0]))

        k = cv2.waitKey(0)
        if k > 47 and k < 58:
            savevar = True
            for _ in range(5): traindata, traindata_labels = imglearn(test_img_rs, k, traindata, traindata_labels)
    
    cv2.destroyAllWindows()
    if savevar:
        np.savez(ocrdata, train=traindata, train_labels=traindata_labels)

Mode = 3

if Mode == 1: # First Study 
    main()
elif Mode == 2: # Recognition Study
    main()
elif Mode == 3: # Module 
    pass
