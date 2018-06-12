from tkinter import *
import PIL.Image, PIL.ImageTk
import cv2 as cv
import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

class MainWindow():

    def __init__(self, main):
        self.canvas = Canvas(main, width=1100, height=500)
        self.canvas.grid(row=0, column=0)
        self.img_list = []

    def load_images(self):
        with open('book1.csv') as csv_file:
            fields=['name', 'objs']
            reader = csv.DictReader(csv_file, fieldnames=fields)
            for row in reader:
                tp_img = (row['name'], row['objs'])
                self.img_list.append(tp_img)


class Rect:
    idx = -1
    x = None
    y = None
    w = None
    h = None

    def str2float(self, s):
        def char2num(s):
            return {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}[s]
             #这事实上是一个字典
        index_point=s.find('.')
        if index_point==-1:
            daichu=1
        else:
            daichu=0.1**(len(s)-1-index_point)
            s=s[0:index_point]+s[index_point+1:]#这里是除去小数点
        from functools import reduce
        result1=reduce(lambda x,y:x*10+y,map(char2num,s))
        return result1*daichu

    def __init__(self,idx, str):
        self.idx = idx
        l = str.split('_')
        print(l)
        self.x = int(self.str2float(l[0]))
        self.y = int(self.str2float(l[1]))
        self.w = int(self.str2float(l[2]))
        self.h = int(self.str2float(l[3]))

    def draw_me(self, image):
        cv.rectangle(image, (self.x,self.y),(self.x+self.w, self.y+self.h), (0, 255,0) )

        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(image, str(self.idx), (self.x + int(self.w/2), self.y+int(self.h/2)), font, 1, (0, 255, 0), 1, cv.LINE_AA)

    def print_me(self):
        print("x,y, w, h: %d, %d, %d, %d"%(self.x,self.y,self.w,self.h))


class CarImage:

    def __init__(self):
        self.img_list = []
        self.out_list = []

    def load_csv(self, path):
        with open(path) as csv_file:
            fields=['name', 'objs']
            reader = csv.DictReader(csv_file, fieldnames=fields)
            for row in reader:
                tp_img = (row['name'], row['objs'])
                self.img_list.append(tp_img)

    def num_images(self):
        return len(self.img_list)

    def get_image(self, idx):
        item = self.img_list[idx]
        if item is None:
            return ;
        return item

window = Tk()

#load all images
carImgs = CarImage()
carImgs.load_csv('book1.csv')

#display the 1st image
item = carImgs.get_image(0)
cv_img = cv.cvtColor(cv.imread('images//' + item[0]), cv.COLOR_BGR2RGB)
width = 1068
height = 500
canvas = Canvas(window, width= width, height=height)
canvas.pack()
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
canvas.create_image(0, 0, image=photo, anchor=NW)

def helloCallBack():
    item = carImgs.get_image(1)
    cv_img = cv.cvtColor(cv.imread('images//' + item[0]), cv.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    canvas.create_image(0, 0, image=photo, anchor=NW)

#put  button, text
catg = [ 'car', 'bus', 'truck']
list_cat  = Listbox(window)
for item in catg:                 # 第一个小部件插入数据
    list_cat.insert(0,item)
list_cat.pack()

btn_next = Button(window, text ="Next", command = helloCallBack)
btn_next.pack()

window.mainloop()
