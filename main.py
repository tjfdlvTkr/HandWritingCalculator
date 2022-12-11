from tkinter import *
import cv2
from PIL import Image, ImageTk

from detect import *
from formula import *

window = Tk()
window.title("Handwriting Recognition Calculator")
window.geometry("800x680")

def exit_window():
    window.destroy()

blank_label = Label(window, height=1)
blank_label.pack()

# Create a Label to capture the Video frames
label = Label(window)
label.pack()
cap= cv2.VideoCapture(0)

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Define function to show frame
def show_frames():
    global orig_image
    # Get the latest frame and convert into Image
    orig_image= cap.read()[1]
    cv2image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Repeat after an interval to capture continiously
    label.after(50, show_frames)

show_frames()

label_for_p = Label(window, width=70, height=10)
label_for_p.pack()

label_for = Label(label_for_p, text="Formula : ", font=('나눔고딕', 16))
label_for.pack(side="left")

ent_for = Entry(label_for_p, font=('나눔고딕',16),bg='white',width=40)
ent_for.pack(side="left")

string = ""

def captureImg():
    global ent_for
    global string

    fname = '_log/capture.png'
    cv2.imwrite(fname, orig_image)
    ent_for.delete(0,"end")

    string = detFormula(fname)
    ent_for.insert(0, string)

label_for_ui = Label(window, width=80, height=10)
label_for_ui.pack()

button_cap = Button(label_for_ui,text="Capture",font=('나눔고딕',16,'bold'),width=8,command=captureImg)
button_cap.pack(side="left")

label_for_ui_for_blank1 = Label(label_for_ui, width=2)
label_for_ui_for_blank1.pack(side="left")

def calcAnswer():
    global label_for_resultString
    global string
    global ent_for

    string = ent_for.get()
    label_for_resultString.config(text=str(strcar(string)))

button_cal = Button(label_for_ui,text="Calculate",font=('나눔고딕',16,'bold'),width=8,command=calcAnswer)
button_cal.pack(side="left")


label_for_result = Label(window, text="- Result -", font=('나눔고딕', 16))
label_for_result.pack()

label_for_resultString = Label(window, text="", font=('나눔고딕', 16))
label_for_resultString.pack()

window.protocol('WM_DELETE_WINDOW', exit_window)

window.mainloop()