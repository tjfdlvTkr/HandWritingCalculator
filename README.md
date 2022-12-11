# Handwriting Recognition Calculator with OpenCV

When you show a handwritten formula on the screen, it recognizes it and calculates the formula.

The user UI was created using [opencv](https://github.com/opencv/opencv) and tkinter, and the webcam is recognized using [opencv](https://github.com/opencv/opencv). The kNN algorithm is used to separate numbers and operators and express them as expressions for calculations. The numeric and operator data sets were hand-generated.

### Repository
- detect.py : Explore the number field in a photo.
- digit_study.py : Learn numbers or derive results.
- formula.py : Calculate Formula ( strcar function module )
- main.py 

### Requirements
The following libraries are required to run the program.
```sh
pip install opencv-python
pip install tk
pip install pillow
pip install numpy
```

The following is the environment in which this source code was compiled.
```sh
Python 3.11.1
opencv-python 4.6.0
Tkversion 8.6
numpy 1.23.5
pillow 9.3.0
```

### Usage
1. Run main.py.
2. Save the picture from your webcam with the Capture button.
3. Calculate the formula with the Calculate button.

<span>
  <img src="https://github.com/tjfdlvTKr/HandWritingCalculator/blob/main/README_img/img1.png" width="350" align="left"/>
  <img src="https://github.com/tjfdlvTkr/HandWritingCalculator/blob/main/README_img/img2.png" width="350"/>
</span>  
<p></p>

### Limitations
1. Numeric and operator extraction does not have high accuracy. You can edit recognized formulas in Formula Entry.
2. Recognition may not be performed if other characters or backgrounds are visible.
3. We are considering an alternative way to upload photos if you do not have a webcam installed.
4. We are considering adding additional types of operations.

### References
* [머신러닝 기초2 - kNN을 이용하여 손글씨 인식하기](https://blog.naver.com/samsjang/220684292757)
* [Text Detection and Extraction using OpenCV and OCR](https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/)
