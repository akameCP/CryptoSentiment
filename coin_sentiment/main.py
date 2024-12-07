

from gui import LoginApp
from PyQt5.QtWidgets import QApplication



def gui():
    app = QApplication([])
    login_window = LoginApp()
    login_window.show()
    app.exec_()
    
def main():
    gui()
    
if __name__ == "__main__":
    main()