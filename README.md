# face-recognition

## Description

Face-recognition is repository with three main programs. First is the **face_capture.py** program which simply detects a human face real-time, takes a screenshot for every fifth frame, and saves all the images in a directory called "output". The program uses a pre-existing face-detector, which is included in the "opencv_face_detector" directory in this repository. The second program is a Jupyter Notebook file, **Face_Recognition.ipynb**, that constructs a CNN (Convolutional Neural Network) model and trains it to recognize my own face. The datasets used here were (1) [Flickr-Face-HQ-Dataset](https://github.com/NVlabs/ffhq-dataset) and (2) the images of my face I created using face_capture.py program.

The last program is **face_recog.py** which is capable of accurately recognizing and distinguishing my face from other human faces. It uses a frozen graph created by the Face_Recognition.ipynb file to accurately detect my face and distinguish it from other human faces. The program will label my face with a green border-box and label other human faces with red ones.

The objective of the face-recognition project was to apply fundamental deep learning knowledge to create a personalized CNN model. The biggest challenge here was the process of creating and transferring the frozen graph from Jupyter Notebook to use it on real-time command program. Further improvements can be made by increasing the sample size of the datasets (more face captures) and exploring with transfer learning to train the model to recognize my face.

## Installation

I used the OpenCV package for python (version 4.1.0.25 or above) with Python 3.7.2

```bash
pip install opencv-python==4.1.0.25
```

## Usage

Clone the face-recognition repository in your directory.

```bash
git clone https://github.com/byunsy/face-recognition.git
```

Move to your specific directory and execute the program.

```bash
python face_recog.py
```

## Demonstrations

The program can accurately recognize my face and distinguish it from other human faces.

![](images/face_rec.gif)
