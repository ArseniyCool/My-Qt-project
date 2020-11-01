import winsound
import sys
from PyQt5 import uic
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design of test.ui', self)
        self.setWindowTitle('Design of test New')

        f = open("file_of_words.txt", "r",  encoding="utf-8").read().split()
        print(f)
        # self.button.clicked.connect(partial(self.usual_button_click, '0-1'))
        # self.count = 0
        #
        # self.like_button.clicked.connect(partial(self.like_button_click, '2-3'))
        # self.adore_button.clicked.connect(partial(self.adore_button_click, '4-5'))
        self.buttons = []
        self.counts = []
        self.nums = []
        self.favourite = True
        # self.frame.hide()
        x, y, = 70, 70
        self.num = 1
        for i in range(len(f)):
            self.button = QPushButton(f[i], self)
            if len(f[i]) <= 4:
                self.num = 18
            elif len(f[i]) <= 6:
                self.num = 14
            elif len(f[i]) <= 10:
                self.num = 11
            elif len(f[i]) <= 15:
                self.num = 9
            else:
                self.num = 5
            self.nums.append(self.num)
            self.button.setStyleSheet(f'''background-color: rgb(215, 255, 165); 
                                         color: rgb(0, 0, 0);
                                         font: {self.num}pt "Times New Roman";
                                         border-radius: 30px 30px;''')
            self.button.clicked.connect(self.button_click)
            self.counts.append(0)
            self.button.resize(60, 60)
            self.button.move(x, y)
            if x == 520:
                y += 150
                x = 70
            else:
                x += 150
            self.buttons.append(self.button)
    # TODO: Кнопки "Готово" и "Отмена", взаимосвзязь кнопок и прогресс бара с текстом,
    #  отдельный фрейм для показа результата, сам вывод результата тестирования
    # TODO: Другое
    #  -СДЕЛАНО-: Принятие списка из файла, рабочие кнопки теста, звук нажатия кнопки
    #  через модуль winsound (Другое), кнопка "Фаворит" (Другое)

    def button_click(self):
        sender = self.sender()
        index = self.buttons.index(sender)
        if self.counts[index] == 0:
            MyWidget.usual_button_click(self, sender, index)
        elif self.counts[index] < 3:
            MyWidget.like_button_click(self, sender, index)
        elif self.counts[index] < 5:
            MyWidget.adore_button_click(self, sender, index)
        elif self.favourite:
            self.favourite = False
            winsound.PlaySound('sounds/pushbutton.wav', winsound.SND_ASYNC)
            MyWidget.favour_button_click(self, sender, index)
        if self.counts[index] != 5:
            winsound.PlaySound('sounds/pushbutton.wav', winsound.SND_ASYNC)
            self.counts[index] += 1

    def usual_button_click(self, sender, index):
        sender.resize(70, 70)
        print(self.counts[index])
        sender.move(sender.x() - 5, sender.y() - 5)
        sender.setStyleSheet(f'''background-color: rgb(178, 255, 89);
                                color: rgb(0, 0, 0);
                                font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                border-radius: 35px 35px;''')

    def like_button_click(self, sender, index):
        if self.counts[index] == 1:
            sender.resize(80, 80)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(115, 236, 38);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 40px 40px;''')
        else:
            sender.resize(90, 90)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(100, 221, 23);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 45px 45px;''')

    def adore_button_click(self, sender, index):
        if self.counts[index] == 3:
            sender.resize(100, 100)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(255, 82, 82);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 50px 50px;''')
        else:
            sender.resize(110, 110)
            sender.move(sender.x() - 5, sender.y() - 5)
            print(sender.x())
            sender.setStyleSheet(f'''background-color: rgb(255, 23, 68);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 55px 55px;''')

    def favour_button_click(self, sender, index):
        sender.resize(120, 120)
        sender.move(sender.x() - 5, sender.y() - 5)
        sender.setStyleSheet(f'''background-color: rgb(255, 245, 0);
                                color: rgb(0, 0, 0);
                                font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                border-radius: 60px 60px;''')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
