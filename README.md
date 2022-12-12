# Handwriting Recognition Calculator with OpenCV

When you show a handwritten formula on the screen, it recognizes it and calculates the formula.

The user UI was created using [opencv](https://github.com/opencv/opencv) and tkinter, and the webcam is recognized using [opencv](https://github.com/opencv/opencv). The kNN algorithm is used to separate numbers and operators and express them as expressions for calculations. The operator data sets were hand-generated. The numerical data set used the MNIST dataset.

### Repository
- detect.py : Explore the text field in a photo.
- digit_study.py : Learn character or derive results.
- formula.py : Calculate Formula ( strcar function module )
- keras_digit.py : Learn digit or derive results.
- main.py 

### Requirements
The following libraries are required to run the program.
```sh
pip install opencv-python
pip install tk
pip install pillow
pip install numpy
pip install keras
pip install tensorflow
```

The following is the environment in which this source code was compiled.
```sh
Python 3.9.1
opencv-python 4.6.0
tk 0.1.0
numpy 1.23.5
pillow 9.3.0
keras 2.11.0
tensorflow 2.11.0
```

### Usage
1. Run main.py.
2. Save the picture from your webcam with the Capture button.
3. Calculate the formula with the Calculate button.

> Currently available operations are addition, subtraction, multiplication, division and parentheses operations.
> You can enter the following command. : +, -, x, /, (, )

<span>
  <img src="https://github.com/tjfdlvTKr/HandWritingCalculator/blob/main/README_img/img1.png" width="350" align="left"/>
  <img src="https://github.com/tjfdlvTkr/HandWritingCalculator/blob/main/README_img/img2.png" width="350"/>
</span>  
<p></p>

### Limitations
1. Numeric and operator extraction does not have high accuracy. You can edit recognized formulas in Formula Entry.
2. Recognition may not be performed if other characters or backgrounds are visible.
3. Recognition may not be possible if the font thickness or size is small.
4. We are considering an alternative way to upload photos if you do not have a webcam installed.
5. We are considering adding additional types of operations.

### References
* [머신러닝 기초2 - kNN을 이용하여 손글씨 인식하기](https://blog.naver.com/samsjang/220684292757)
* [Text Detection and Extraction using OpenCV and OCR](https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/)
* [Mnist handwritten digit classification using tensorflow](https://www.milindsoorya.com/blog/handwritten-digits-classification)

### Contribute
Modification is possible after fork operation. The main creators of that open source are: [tjfdlvTkr](https://github.com/tjfdlvTkr), [jeonggeun105](https://github.com/jeonggeun105)