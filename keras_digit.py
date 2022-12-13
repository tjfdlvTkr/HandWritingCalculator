from keras.utils import np_utils
from keras.models import load_model

import numpy as np
import cv2

# MNIST model to improve the accuracy of digit recognition
def keras_predict():
    img = cv2.imread('_log/dig.png')
    model = load_model('Keras_Model.h5')

    # Image reshape with 784 pixels
    test_num = cv2.resize(img, (28,28))[:,:,1]
    test_num = (test_num < 70) * test_num
    test_num = test_num.astype('float32') / 255.
    test_num = test_num.reshape((-1, 28 * 28))

    # Number prediction
    predicted = model.predict(test_num)
    predicted_num = np.argmax(predicted, axis=-1)
    return predicted_num[0]