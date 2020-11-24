import winsound
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

WHITE = 'rgb(255, 255, 255)'
BLACK = 'rgb(0, 0, 0)'
COLOR = ['rgb(215, 255, 165)', 'rgb(178, 255, 89)', 'rgb(115, 236, 38)', 'rgb(100, 221, 23)',
         'rgb(255, 82, 82)', 'rgb(255, 23, 68)', 'rgb(255, 245, 0)']
# TODO: ВСЕ ГОТОВО, ПЕРЕХОЖУ КО 2 ФАЗЕ (Регистрация, база данных, исправление недочетов, дизайн)
#  -СДЕЛАНО-: Принятие списка из файла - теперь позволяет выбрать любой файл .txt пользователю,
#  созданы исключения на выбор файла (Другое), рабочие кнопки теста: исправлены ошибки в шрифте
#  звук нажатия кнопки через модуль winsound (Другое), кнопка "Фаворит" (Другое)
#  Кнопки "Настроек" - "Готово", "Сбросить" и "Отмена"(Другое), налажена работа кнопок
#  "Настроек" (теперь кнопки можно нажать только при определнных обстоятельствах, например: кнопку
#  "Готово" после нажатия  всех необх. кнопок) (Другое), взаимосвзязь кнопок
#  и прогресс бара прогресс бара с текстом, отдельный фрейм для показа результата,
#  сам вывод результата тестирования


class FileError(Exception):
    pass


class WordCountError(FileError):
    pass


class LengthWordError(FileError):
    pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design of test.ui', self)
        self.setWindowTitle('Design of test New')
        self.text_file = QFileDialog.getOpenFileName(
            self, 'Выбрать список', '',
            'Текстовый файл (*.txt)')[0]
        self.f = open(self.text_file, "r", encoding="utf-8").read().split()
        if len(self.f) < 3:  # проверка списка на наличие хотя бы 3 элементов
            raise WordCountError("Ошибка! Ваш файл должен содержать минимум 3 элемента")

        self.buttons = []
        self.counts = []
        self.nums = []
        self.favourite = True
        self.end = False
        self.push_need = round(0.5 * (5 * len(self.f) + 1))  # кол-во необходимых нажатий на кнопку
        # вычисляется по формуле: "процент_необходимых нажатий * максимально_возможное_кол-во_нажатий
        self.push_count = 0
        self.completed = 0

        self.test_info.setText(f'НАЖМИТЕ ЕЩЕ НА {self.push_need - self.push_count} КНОПОК')
        self.progress.setValue(self.completed)
        self.backward.setEnabled(False)
        self.ready.setEnabled(False)
        self.drop.setEnabled(False)
        self.last_number = 0
        self.last_index = 0
        # self.frame.hide()
        self.drop.clicked.connect(self.dropping)
        self.backward.clicked.connect(self.backward_event)
        self.ready.clicked.connect(self.ready_event)
        x, y, = 70, 70
        self.num = 1
        for i in range(len(self.f)):
            if len(self.f[i]) > 16:
                raise WordCountError("Ошибка! Ваш файл должен содержать минимум 3 элемента")
                # проверка количества букв в слове (макс. 16)
            self.button = QPushButton(self.f[i], self)
            if len(self.f[i]) <= 4:
                self.num = 18
            elif len(self.f[i]) <= 6:
                self.num = 14
            elif len(self.f[i]) <= 8:
                self.num = 11
            elif len(self.f[i]) <= 16:
                self.num = 9
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

    def button_click(self):
        sender = self.sender()
        index = self.buttons.index(sender)
        if self.end or (not self.favourite and 5 <= self.counts[index] <= 7):
            return
        else:
            self.push_count += 1
            self.completed = round((self.push_count / self.push_need) * 100)
            self.progress.setValue(self.completed)
            self.backward.setEnabled(True)
            self.backward.setStyleSheet(f'''background-color: rgb(68, 138, 255);
                                                        color: rgb(255, 255, 255);''')
        self.last_button = self.sender()
        self.last_index = index
        if self.push_need == self.push_count:
            self.test_info.setText('ГОТОВО')
            winsound.PlaySound('sounds/pushbutton.wav', winsound.SND_ASYNC)
            self.end = True
            self.ready.setEnabled(True)
            self.ready.setStyleSheet(f'''background-color: rgb(68, 138, 255);
                                                    color: rgb(255, 255, 255);''')
        else:
            self.test_info.setText(f'НАЖМИТЕ ЕЩЕ НА {self.push_need - self.push_count} КНОПОК')
        if self.counts[index] == 0:
            self.drop.setEnabled(True)
            self.drop.setStyleSheet(f'''background-color: rgb(68, 138, 255);
                                                color: rgb(255, 255, 255);''')
            MyWidget.usual_button_click(self, sender, index)
        elif self.counts[index] < 3:
            MyWidget.like_button_click(self, sender, index)
        elif self.counts[index] < 5:
            MyWidget.adore_button_click(self, sender, index)
        elif self.counts[index] == 5:
            if self.favourite:
                self.favourite = False
                winsound.PlaySound('sounds/pushbutton.wav', winsound.SND_ASYNC)
                MyWidget.favour_button_click(self, sender, index)
            else:
                return
        if self.counts[index] != 5:
            winsound.PlaySound('sounds/pushbutton.wav', winsound.SND_ASYNC)
            self.counts[index] += 1

    def usual_button_click(self, sender, index):
        self.last_number = 0
        sender.resize(70, 70)
        sender.move(sender.x() - 5, sender.y() - 5)
        sender.setStyleSheet(f'''background-color: rgb(178, 255, 89);
                                color: rgb(0, 0, 0);
                                font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                border-radius: 35px 35px;''')

    def like_button_click(self, sender, index):
        if self.counts[index] == 1:
            self.last_number = 1
            sender.resize(80, 80)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(115, 236, 38);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 40px 40px;''')
        else:
            self.last_number = 2
            sender.resize(90, 90)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(100, 221, 23);
                                    color: rgb(0, 0, 0);
                                    font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                    border-radius: 45px 45px;''')

    def adore_button_click(self, sender, index):
        if self.counts[index] == 3:
            self.last_number = 3
            sender.resize(100, 100)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(255, 82, 82);
                                    color: rgb(255, 255, 255);
                                    font: {self.nums[index] + self.counts[index] + 1}pt 
                                    "Times New Roman";
                                    border-radius: 50px 50px;''')
        else:
            self.last_number = 4
            sender.resize(110, 110)
            sender.move(sender.x() - 5, sender.y() - 5)
            sender.setStyleSheet(f'''background-color: rgb(255, 23, 68);
                                    color: rgb(255, 255, 255);
                                    font: {self.nums[index] + self.counts[index] + 1}pt 
                                    "Times New Roman";
                                    border-radius: 55px 55px;''')

    def favour_button_click(self, sender, index):
        self.last_number = 5
        self.counts[index] += 1
        sender.resize(120, 120)
        sender.move(sender.x() - 5, sender.y() - 5)
        sender.setStyleSheet(f'''background-color: rgb(255, 245, 0);
                                color: rgb(0, 0, 0);
                               font: {self.nums[index] + self.counts[index] + 1}pt "Times New Roman";
                                border-radius: 60px 60px;''')

    def dropping(self):
        if self.end:
            self.ready.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                         color: rgb(255, 255, 255);''')
            self.ready.setEnabled(True)
        self.drop.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                    color: rgb(255, 255, 255);''')
        self.drop.setEnabled(False)
        self.backward.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                                color: rgb(255, 255, 255);''')
        self.backward.setEnabled(False)
        self.last_number = 0
        self.end = False
        self.favourite = True
        self.push_count = 0
        self.completed = 0
        self.test_info.setText(f'НАЖМИТЕ ЕЩЕ НА {self.push_need - self.push_count} КНОПОК')
        self.progress.setValue(self.completed)
        x, y, = 70, 70
        for i in range(len(self.f)):
            self.button = self.buttons[i]
            if len(self.f[i]) <= 4:
                self.num = 18
            elif len(self.f[i]) <= 6:
                self.num = 14
            elif len(self.f[i]) <= 8:
                self.num = 11
            elif len(self.f[i]) <= 15:
                self.num = 9
            else:
                self.num = 5
            self.nums[i] = self.num
            self.button.setStyleSheet(f'''background-color: rgb(215, 255, 165); 
                                         color: rgb(0, 0, 0);
                                         font: {self.num}pt "Times New Roman";
                                         border-radius: 30px 30px;''')
            self.counts[i] = 0
            self.button.resize(60, 60)
            self.button.move(x, y)
            if x == 520:
                y += 150
                x = 70
            else:
                x += 150

    def backward_event(self):
        if self.end:
            self.ready.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                         color: rgb(255, 255, 255);''')
            self.ready.setEnabled(False)
            self.end = False
        self.push_count -= 1
        self.completed = round((self.push_count / self.push_need) * 100)
        self.test_info.setText(f'НАЖМИТЕ ЕЩЕ НА {self.push_need - self.push_count} КНОПОК')
        self.progress.setValue(self.completed)
        if self.push_count == 0:
            self.drop.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                        color: rgb(255, 255, 255);''')
            self.drop.setEnabled(False)

        text_color = WHITE if 3 < self.last_number <= 5 else BLACK
        if self.last_number == 5:
            self.favourite = True
            self.counts[self.last_index] += 1
        self.last_button.resize(self.last_number * 10 + 60, self.last_number * 10 + 60)
        self.last_button.move(self.last_button.x() + 5, self.last_button.y() + 5)
        self.last_button.setStyleSheet(f'''background-color: {COLOR[self.last_number]}; 
                                           color: {text_color};
                                           font: {self.nums[self.last_index] + self.last_number}pt "Times New Roman";
                                           border-radius: {self.last_number * 5 + 30}px {self.last_number * 5 + 30}px;''')
        self.backward.setEnabled(False)
        self.counts[self.last_index] -= 1
        self.backward.setStyleSheet(f'''background-color: rgb(171, 171, 171);
                                        color: rgb(255, 255, 255);''')

    def ready_event(self):
        breaking = False
        for i in range(len(self.counts)):
            row = []
            num = f'{i + 1} место)'
            for j in range(self.counts.count(max(self.counts))):
                ind = max(self.counts)
                if ind == -1:
                    breaking = True
                    break
                a = self.counts.index(ind)
                if self.favourite:
                    num = 'Фаворит: '
                row.append(self.f[a])
                self.counts[a] = -1
            if breaking:
                break
            self.listWidget.addItem(f"{num} {', '.join(row)}")



try:
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = MyWidget()
        ex.show()
        sys.exit(app.exec_())
except Exception as error:
    print(error)
