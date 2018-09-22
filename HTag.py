import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTranslator

from gui.mainwindow import Ui_MainWindow
from libs.Common import Config


class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.push_button_test)

    def push_button_test(self):
        print('test')

# def main():
#     # db = Database.TagDatabase("data.db")
#     db = Database.TagDatabase(":memory:")
#     if not db.is_database_exist():
#         db.build_database()


if __name__ == '__main__':

    # read config
    try:
        config = Config.get_config()
        if config is None:
            config = Config.create_config()
    except IOError:
        print('Error while reading config', sys.stderr)
        sys.exit()

    app = QApplication(sys.argv)

    trans = QTranslator()
    trans.load('res/local/' + config['DEFAULT']['language'])
    app.installTranslator(trans)

    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
