import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PrimaryUI import PrimaryWindow
import sys

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    window = PrimaryWindow(size.width(), size.height())
    sys.exit(app.exec_())
