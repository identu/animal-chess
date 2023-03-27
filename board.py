import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon
import numpy as np
#使用行列坐标,(3,4)代表第三行第四列

class chessman:
    def __init__(self,status,x,y):
        self.status=status
        self.x=x
        self.y=y

class ChessBoard(QWidget):
    buttons=[]  #存储按钮对象
    status=[]
    selectedButton=None
    grid = QGridLayout()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Animal Chess')
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon('icon.png'))


        self.setLayout(self.grid)

        for i in range(9):  #9行
            self.buttons.append([])  #存储所有按钮（用按钮表示格子（棋子））
            self.status.append([10,10,10,10,10,10,10])  #表示格子的状态，没有棋子的格子状态为10

            for j in range(7):  #7列
                button = QPushButton()
                button.setMinimumSize(75, 75)

                if i>=3 and i<6 and j>=1 and j<=5 and j!=3 :
                    button.setStyleSheet('background-color: blue;font-size:40px')
                else:
                    if i==0 and j==3 or i==8 and j==3:
                        button.setStyleSheet('font-size:40px')#'background-color: yellow;font-size:40px')
                    else:
                        button.setStyleSheet('background-color: #82e571;font-size:40px')#'background-color: #82e571;font-size:40px')
                self.grid.addWidget(button, i, j)
                self.buttons[i].append(button)
                button.clicked.connect(self.buttonClicked)
#                print(self.getButtonPosition(button))

    def setChessMan(self): #摆棋子
        name=['狮','井','井','虎','狗','井','猫','鼠','豹','狼','象']  #象狮虎豹狗狼猫鼠98765432 进入陷阱的棋子为1
        order=[8, 0, 0, 7, 4, 0, 3, 2, 6, 5, 9]  #井0 空10
        for i in range(0,21,2):
            self.buttons[int(i/7)][i%7].setText(name[int(i/2)])
            self.buttons[int(i/7)][i%7].setStyleSheet("background-color: #82e571;font-size:40px;color:blue")
            self.status[int(i/7)][i%7]=order[int(i/2)]
        order1=[-8,0,0,-7,-4,0,-3,-2,-6,-5,-9]
        for i in range(62,40,-2):
            self.buttons[int(i/7)][i%7].setText(name[10-int((i-42)/2)])
            self.buttons[int(i/7)][i%7].setStyleSheet("background-color: #82e571;font-size:40px;color:red")
            self.status[int(i/7)][i%7]=order1[10-int((i-42)/2)]




    def getButtonPosition(self,button):  #返回行列坐标
        for i in range(9):
            if button in self.buttons[i]:
                return i,self.buttons[i].index(button)


    def buttonClicked(self):  #点击事件
        button = self.sender()  # 获取点击的按钮


        row,col=self.getButtonPosition(button)
        if not self.selectedButton:  # 如果没有选中的按钮
            if self.hasChessman(row,col):  # 如果该按钮上有棋子
                self.selectedButton = button  # 选中该按钮
                print('select',row,col)
            else:
                print('点击空')
        else:  # 如果已经选中了一个按钮
            if self.isValidMove(row,col):  # 如果目标位置是有效的移动位置
                self.moveChessman(row,col)  # 移动棋子
            self.selectedButton = None  # 取消选中的按钮


    def hasChessman(self, row, col):
        return self.status[row][col] != 10 and self.status[row][col] != 0

    def isValidMove(self, row, col):
        row0,col0=self.getButtonPosition(self.selectedButton)
        c2=self.status[row][col]  #目标棋子
        c1=self.status[row0][col0]  #原棋子
        if c1==10 or c1==0:#空或井不能动
            return False
        if row==row0 and abs(col-col0)==1 or col==col0 and abs(row-row0)==1:  #每次只能移动1格

            if self.status[row][col] == 10 and self.status[row0][col0] < 10:
                return True
            else:
                if c1*c2<=0:
                    if abs(c1)==2 and abs(c2)==9:  #鼠吃象规则，首先判断
                        return True
                    if abs(c1)>=abs(c2) and not (abs(c1)==9 and abs(c2)==2):
                        return True
                else:
                    return False
        else:
            return False


    def moveChessman(self, row, col):
        trap=[]
        text=self.selectedButton.text()
        row0,col0=self.getButtonPosition(self.selectedButton)   #棋子原行列坐标
        print(text+" move to",row,col)
        style=self.selectedButton.styleSheet()  #获取样式表
        print(style)
        style1=self.sender().styleSheet()
        print(style1)
        if self.status[row][col]==0:
            self.status[row][col]=np.sign(self.status[row0][col0])  #用符号函数削到1
        else:
            self.status[row][col]=self.status[row0][col0] #移动状态
        if abs(self.status[row0][col0])==1: #要从陷阱里出来
            self.status[row0][col0]=0
        self.status[row0][col0]=10
        self.selectedButton.setText('') #移动文字
        self.buttons[row][col].setText(text)
        self.selectedButton.setStyleSheet(style1)#移动样式
        self.sender().setStyleSheet(style)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = ChessBoard()
    board.show()
    board.setChessMan()
    sys.exit(app.exec_())

