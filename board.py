import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
import numpy as np


# 使用行列坐标,(3,4)代表第三行第四列

class chessman:
    def __init__(self, status, x, y):
        self.status = status
        self.x = x
        self.y = y


class ChessBoard(QWidget):
    buttons = []  # 存储按钮对象
    status = []
    animals = ['象', '狮', '虎', '豹', '狼', '狗', '猫', '鼠']
    levels = [9, 8, 7, 6, 5, 4, 3, 2]
    selectedButton = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Animal Chess')
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon('icon.png'))

        grid = QGridLayout()
        self.setLayout(grid)

        for j in range(7):  # 7行
            self.buttons.append([])  # 存储所有按钮（用按钮表示格子（棋子））
            self.status.append([10, 10, 10, 10, 10, 10, 10, 10, 10, 10])  # 表示格子的状态，没有棋子的格子状态为10

            for i in range(9):  # 9列
                button = QPushButton()
                button.setMinimumSize(75, 75)

                if 6 > i >= 3 != j and 1 <= j <= 5:
                    button.setStyleSheet('background-color: cornflowerblue;font-size:40px')
                else:
                    button.setStyleSheet(
                        'background-color: #82e571;font-size:40px')
                grid.addWidget(button, j, i)
                self.buttons[j].append(button)
                button.clicked.connect(self.buttonClicked)

    def setChessMan(self):  # 摆棋子

        name = ['狮', '阱', '阱', '虎', '狗', '阱', '猫', '鼠', '豹', '狼', '象']  # 象狮虎豹狼狗猫鼠98765432 进入陷阱的棋子为1
        order = [8, 0, 0, 7, 4, 0, 3, 2, 6, 5, 9]  # 井0 空10
        for i in range(0, 21, 1):
            if i % 2 == 0:
                self.buttons[i % 7][int(i / 7)].setText(name[int(i / 2)])
                self.status[i % 7][int(i / 7)] = order[int(i / 2)]
            self.buttons[i % 7][int(i / 7)].setStyleSheet("background-color: #82e571;font-size:40px;color:blue")
        self.buttons[3][0].setText('穴')
        order1 = [-8, 0, 0, -7, -4, 0, -3, -2, -6, -5, -9]
        for i in range(62, 40, -1):
            if i % 2 == 0:
                self.buttons[i % 7][int(i / 7)].setText(name[10 - int((i - 42) / 2)])
                self.status[i % 7][int(i / 7)] = order1[10 - int((i - 42) / 2)]
            self.buttons[i % 7][int(i / 7)].setStyleSheet("background-color: #82e571;font-size:40px;color:red")
        self.buttons[3][8].setText('穴')

    def getButtonPosition(self, button):  # 返回行列坐标
        for i in range(7):
            if button in self.buttons[i]:
                return i, self.buttons[i].index(button)

    def buttonClicked(self):  # 点击事件
        button = self.sender()  # 获取点击的按钮
        row, col = self.getButtonPosition(button)
        if not self.selectedButton:  # 如果没有选中的按钮
            if self.hasChessman(row, col):  # 如果该按钮上有棋子
                self.selectedButton = button  # 选中该按钮
                print('选中', button.text())
            else:
                print('点击空')
        else:  # 如果已经选中了一个按钮
            if self.isValidMove(row, col):  # 如果目标位置是有效的移动位置
                self.moveChessman(row, col)  # 移动棋子
            self.selectedButton = None  # 取消选中的按钮

    def hasChessman(self, row, col):
        return self.status[row][col] != 10 and self.status[row][col] != 0  # 不是空地或陷阱

    def isValidMove(self, row, col):
        row0, col0 = self.getButtonPosition(self.selectedButton)
        c2 = self.status[row][col]  # 目标棋子
        c1 = self.status[row0][col0]  # 原棋子
        if c1 == 10 or c1 == 0:  # 空或井不能动
            return False
        if row == row0 and abs(col - col0) == 1 or col == col0 and abs(row - row0) == 1:  # 每次只移动1格
            # 不能进入己方兽穴
            if c1 < 0 and row == 3 and col == 8 or c1 > 0 and row == 3 and col == 0:
                return False
            if c2 == 10 and c1 < 10:
                if 1 <= row <= 5 and row != 3 and 3 <= col <= 5:  # 鼠走河
                    if abs(c1) == 2:
                        return True
                    else:
                        return False
                return True
            else:
                if c1 * c2 <= 0:

                    if abs(c1) == 2 and abs(c2) == 9:  # 鼠吃象规则
                        if 1 <= row0 <= 5 and row0 != 3 and 3 <= col0 <= 5:
                            return False
                        return True
                    if abs(c1) >= abs(c2) and not (abs(c1) == 9 and abs(c2) == 2):
                        if 1 <= row <= 5 and row != 3 and 3 <= col <= 5:  # 鼠走河
                            if abs(c1) == 2:
                                return True
                            else:
                                return False
                        return True
                    return False
                else:
                    return False
        else:
            # 跳河规则
            if abs(c1) == 8 or abs(c1) == 7:
                if c1 * c2 <= 0 and abs(c1) >= abs(c2) or c1 != 10 and c2 == 10:
                    if (col0 == 2 and col == 6 or col0 == 6 and col == 2) and row0 == row and 1 <= row <= 5 and row != 3:  # 横跳
                        if self.status[row0][3] == self.status[row0][4] and self.status[row0][4] == self.status[row0][5] and self.status[row0][3] == 10:
                            return True
                        else:
                            return False
                    if (row0 == 0 and row == 3 or row0 == 3 and row == 0 or row0 == 3 and row == 6 or row0 == 6 and row == 3) and col == col0 and 3 <= col <= 5:  # 纵跳
                            if row0 == 0 and row == 3 and self.status[1][col0] == self.status[2][col0] and self.status[2][col0] == 10:
                                return True
                            if row0 == 3 and row == 0 and self.status[1][col0] == self.status[2][col0] and self.status[2][col0] == 10:
                                return True
                            if row0 == 3 and row == 6 and self.status[4][col0] == self.status[5][col0] and self.status[5][col0] == 10:
                                return True
                            if row0 == 6 and row == 3 and self.status[4][col0] == self.status[5][col0] and self.status[5][col0] == 10:
                                return True
                            else:
                                return False
            return False

    def moveChessman(self, row, col):
        stat = 10
        in_trap = 0
        text = self.selectedButton.text()
        row0, col0 = self.getButtonPosition(self.selectedButton)  # 棋子原行列坐标
        print(text + " move to", row, col)
        style = self.selectedButton.styleSheet()  # 获取原样式表
        style1 = self.sender().styleSheet()  # 获取目标样式表
        if row == 3 and col == 1 or row == 2 and col == 0 or row == 4 and col == 0 or row == 3 and col == 7 or row == 2 and col == 8 or row == 4 and col == 8:  # 进入陷阱或吃陷阱里的动物
            if self.status[row0][col0] > 0 and col > 4 or self.status[row0][col0] < 0 and col < 4:
                stat = np.sign(self.status[row0][col0])  # 敌方棋子状态变为1
            else:
                stat = self.status[row0][col0]
            self.status[row0][col0] = 10  # 原棋子状态为10
            self.selectedButton.setText('')
        elif row0 == 3 and col0 == 1 or row0 == 2 and col0 == 0 or row0 == 4 and col0 == 0 or row0 == 3 and col0 == 7 or row0 == 2 and col0 == 8 or row0 == 4 and col0 == 8:  # 要从陷阱里出来
            in_trap = 1
            stat = self.levels[self.animals.index(text)] * np.sign(self.status[row0][col0])
            self.status[row0][col0] = 0  # 状态置为阱
            self.buttons[row0][col0].setText('阱')
            if col0 == 7 or col0 == 8:
                self.buttons[row0][col0].setStyleSheet("background-color: #82e571;font-size:40px;color:red")
            else:
                self.buttons[row0][col0].setStyleSheet("background-color: #82e571;font-size:40px;color:blue")

        else:  # 正常走
            stat = self.status[row0][col0]
            self.status[row0][col0] = 10
            self.selectedButton.setText('')

        self.status[row][col] = stat
        self.buttons[row][col].setText(text)
        a = style.split(';')
        b = style1.split(';')
        str = a[0]
        a[0] = b[0]
        b[0] = str
        style = ";".join(b)
        style1 = ";".join(a)
        if in_trap == 0:
            self.buttons[row0][col0].setStyleSheet(style)  # 交换样式
        self.buttons[row][col].setStyleSheet(style1)
        #获胜判断
        if self.status[row][col]<0 and row==3 and col == 0:
            self.win("红")
        if self.status[row][col]>0 and row==3 and col == 8:
            self.win("蓝")

    def win(self,winer):
        result = QMessageBox.information(self, '结束', winer+'方获胜！是否重开？', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            self.setChessMan()
        else:
            exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = ChessBoard()
    board.show()
    board.setChessMan()
    sys.exit(app.exec_())
