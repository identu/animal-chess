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
    animals=['象','狮','虎','豹','狗','狼','猫','鼠']
    levels=[9,8,7,6,5,4,3,2]
    relation=zip(animals,levels)
    selectedButton=None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Animal Chess')
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon('icon.png'))

        grid = QGridLayout()
        self.setLayout(grid)

        for j in range(7):  #7行
            self.buttons.append([])  #存储所有按钮（用按钮表示格子（棋子））
            self.status.append([10,10,10,10,10,10,10,10,10,10])  #表示格子的状态，没有棋子的格子状态为10

            for i in range(9):  #9列
                button = QPushButton()
                button.setMinimumSize(75, 75)

                if i>=3 and i<6 and j>=1 and j<=5 and j!=3 :
                    button.setStyleSheet('background-color: cornflowerblue;font-size:40px')
                else:
                    button.setStyleSheet('background-color: #82e571;font-size:40px')#'background-color: #82e571;font-size:40px')
                grid.addWidget(button, j, i)
                self.buttons[j].append(button)
                button.clicked.connect(self.buttonClicked)

    def setChessMan(self): #摆棋子
        name=['狮','井','井','虎','狗','井','猫','鼠','豹','狼','象']  #象狮虎豹狗狼猫鼠98765432 进入陷阱的棋子为1
        order=[8, 0, 0, 7, 4, 0, 3, 2, 6, 5, 9]  #井0 空10
        for i in range(0,21,1):
            if i%2==0:
                self.buttons[i%7][int(i/7)].setText(name[int(i/2)])
                self.status[i%7][int(i/7)]=order[int(i/2)]
            self.buttons[i%7][int(i/7)].setStyleSheet("background-color: #82e571;font-size:40px;color:blue")
        self.buttons[3][0].setText('穴')
        order1=[-8,0,0,-7,-4,0,-3,-2,-6,-5,-9]
        for i in range(62,40,-1):
            if i%2==0:
                self.buttons[i%7][int(i/7)].setText(name[10-int((i-42)/2)])
                self.status[i%7][int(i/7)]=order1[10-int((i-42)/2)]
            self.buttons[i%7][int(i/7)].setStyleSheet("background-color: #82e571;font-size:40px;color:red")
        self.buttons[3][8].setText('穴')



    def getButtonPosition(self,button):  #返回行列坐标
        for i in range(7):
            if button in self.buttons[i]:
                return i,self.buttons[i].index(button)


    def buttonClicked(self):  #点击事件
        button = self.sender()  # 获取点击的按钮
        print(self.getButtonPosition(button))
        print(button.text())
        row,col=self.getButtonPosition(button)
        print(self.status[row][col])
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
        return self.status[row][col] != 10 and self.status[row][col] != 0 #不是空地或陷阱

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
            #跳河特殊规则
            return False


    def moveChessman(self, row, col):
        stat=10
        text=self.selectedButton.text()
        row0,col0=self.getButtonPosition(self.selectedButton)   #棋子原行列坐标
        print(text+" move to",row,col)
        style=self.selectedButton.styleSheet()  #获取原样式表
        style1=self.sender().styleSheet()  #获取目标样式表
        if self.status[row][col]==0 or self.status[row][col]==1:  #进入陷阱或吃陷阱里的动物
            stat=np.sign(self.status[row0][col0])  #棋子状态变为1
            self.status[row0][col0]=10  #原棋子状态为10
            self.selectedButton.setText('')
        elif abs(self.status[row0][col0])==1:  #要从陷阱里出来
            stat=self.levels[self.animals.index(text)]*self.status[row0][col0]
            self.status[row0][col0]=0  #状态置为井
            self.buttons[row0][col0].setText('井')
            if col0 > 5:
                self.buttons[row0][col0].setStyleSheet("background-color: #82e571;font-size:40px;color:red")
            else :
                self.buttons[row0][col0].setStyleSheet("background-color: #82e571;font-size:40px;color:blue")

        else: # 正常走
            stat=self.status[row0][col0]
            self.status[row0][col0]=10
            self.selectedButton.setText('')

        self.status[row][col]=stat
        self.buttons[row][col].setText(text)
        self.buttons[row0][col0].setStyleSheet(style1)  #交换样式
        self.buttons[row][col].setStyleSheet(style)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = ChessBoard()
    board.show()
    board.setChessMan()
    sys.exit(app.exec_())

