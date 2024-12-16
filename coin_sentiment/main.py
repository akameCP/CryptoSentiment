
from collections import deque
from gui import LoginApp
from PyQt5.QtWidgets import QApplication


def chartsData(new_data):
    charts_data_deque = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], maxlen=10)
    
    removed_data_deque = charts_data_deque.popleft()
    charts_data_deque.append(new_data)
    
    return charts_data_deque

def gui():
    app = QApplication([])
    login_window = LoginApp()
    login_window.show()
    app.exec_()
    
def main():
    gui()
    
if __name__ == "__main__":
    main()