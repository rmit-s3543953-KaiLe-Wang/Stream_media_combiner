'''
Created on Jul 7, 2020

@author: kai
'''

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from view.Sniffer_GUI import Ui_MainWindow
from model.Uri_model import Uri_model
from model.sniffer import Sniffer
from threading import Thread

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
        input_uri = self.Uri_lineEdit.text()
        #passin.append(['received:',input_uri,""])
        self.Status_label.setText("please wait")
        sniffer = Sniffer(input_uri)
        t = Thread(target=sniffer.start(),args=[])
        t.start()
        passin=self.format_uri_link(sniffer.search_resuest())
        self.table_model =Uri_model(passin)
        self.Sniffer_tableView.setModel(self.table_model)
        #print(passin)
        #print(sum(len(x) for x in passin))
        #print(passin[0][1])
    def format_uri_link(self,link_list):
        formatted_list = []
        for link in link_list:
            formatted_list.append(['uri:',str(link),'download'])
        return formatted_list
if __name__ == '__main__':
    main()