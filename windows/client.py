'''
Created on Jul 7, 2020

@author: kai
'''

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from view.Sniffer_GUI import Ui_MainWindow
from PyQt5.Qt import QTableView
from model.Uri_model import Uri_model

def main():
    app = QApplication(sys.argv)
    main_win = mainWin()
    main_win.show()
    sys.exit(app.exec_())

class mainWin(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(mainWin,self).__init__(parent)
        self.setupUi(self)
        self.Start_sniffer_pushButton.clicked.connect(self.start_handler)
        
    def start_handler(self):
        passin =[]
        passin.append(['message',self.Uri_lineEdit.text(),""])
        passin.append(['uri:','http:asdfasdfasdf',"download"])
        self.table_model =Uri_model(passin)
        print(passin)
        print(sum(len(x) for x in passin))
        print(passin[0][1])
        self.Sniffer_tableView.setModel(self.table_model)
        
if __name__ == '__main__':
    main()