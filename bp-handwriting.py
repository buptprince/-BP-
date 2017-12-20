import sys
from  PIL import Image
from PIL import ImageGrab
import numpy as np
from PyQt5 import (QtCore, QtGui, QtWidgets)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import (QPainter, QPen)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys

def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    return table
class Example(QWidget):
    def clear(self):
        self.pos_xy = []
        self.update()
    def jietu(self):
        print ("w")
        bbox=(112,138,600,640)
        image=ImageGrab.grab(bbox)
        image=image.resize((100,100))
        imgry=image.convert('L')
        table = get_bin_table()
        out = imgry.point(table, '1')
        gdata=out.getdata()
        gdata=np.array(gdata)
        rdata=gdata.reshape(out.height,out.width)
        data=np.matrix(rdata)
        result=np.matrix(np.zeros([10,10]))
        print(data)
        for m in range(0,10):
            for n in range(0,10):
                z=0;
                for i in range(10*m,10*(m+1)):
                    for j in range(10*n,10*(n+1)):
                        if(data[i,j]==0):
                            z+=1;
                print(z)
                if(z>5):
                      result[m,n]=1;
                else:
                      result[m,n]=0;
        print(result)

        f=open('C:/Users/Li/Desktop/quizz.txt','a')
          

        for p in range(0,10):
            for q in range(0,10): 
                f.write(str(result[p,q]))
                f.write('   ');
        f.write('\n')
        f.close()

    def __init__(self):
        super(Example, self).__init__()
        #resize设置宽高，move设置位置
        self.resize(500, 600)
        self.move(100, 100)
        self.setWindowTitle("简单的画板3.0")
        #setMouseTracking设置为False，否则不按下鼠标时也会跟踪鼠标事件
        self.btnclear=QtWidgets.QPushButton(self)#绑定Button到窗口  
        self.btnclear.setText("Clear")
        self.btnclear.setGeometry(20,500,200,50)
        self.btnclear.clicked.connect(self.clear)
        self.btnOK=QtWidgets.QPushButton(self)#绑定Button到窗口  
        self.btnOK.setText("OK")
        self.btnOK.setGeometry(280,500,200,50)
        self.btnOK.clicked.connect(self.jietu)
        self.setMouseTracking(False)

        '''
        要想将按住鼠标后移动的轨迹保留在窗体上
        需要一个列表来保存所有移动过的点
        '''
        self.pos_xy = []

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 4, Qt.SolidLine)
        painter.setPen(pen)

        '''
        首先判断pos_xy列表中是不是至少有两个点了
        然后将pos_xy中第一个点赋值给point_start
        利用中间变量pos_tmp遍历整个pos_xy列表
        point_end = pos_tmp
        画point_start到point_end之间的线
        point_start = point_end
        这样，不断地将相邻两个点之间画线，就能留下鼠标移动轨迹了
        '''
        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue
                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
            painter.end()

    def mouseMoveEvent(self, event):
        '''
        按住鼠标移动事件：将当前点添加到pos_xy列表中
        调用update()函数在这里相当于调用paintEvent()函数
        每次update()时，之前调用的paintEvent()留下的痕迹都会清空
        '''
        #中间变量pos_tmp提取当前点

        if event.pos().y()<=500:
            pos_tmp = (event.pos().x(), event.pos().y())
            #pos_tmp添加到self.pos_xy中
            self.pos_xy.append(pos_tmp)
            self.update()

    def mouseReleaseEvent(self, event):
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt_learn = Example()
    pyqt_learn.show()
    app.exec_()