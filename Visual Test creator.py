
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Design of test v1.0.ui', self)
    # TODO: Рабочие кнопки теста, кнопки "Готово" и "Отмена", принятие списка из файла,
    #  отдельный фрейм для показа результата, сам вывод результата тестирования
    # TODO: Другое


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
