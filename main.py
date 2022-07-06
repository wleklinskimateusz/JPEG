from gui import Window, QApplication
import sys


def main():
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
