import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from NULLscan import *
from p1_ack import *

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("scan_design.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ####버튼들 연결
        self.btn_stealth.clicked.connect(self.btnClick_stealth)
        self.btn_ack.clicked.connect(self.btnClick_ack)
        self.btn_ping.clicked.connect(self.btnClick_ping)
        self.btn_reset.clicked.connect(self.btnClick_reset)
        self.btn_banner.clicked.connect(self.btnClick_banner)
    
    def btnClick_reset(self):
        self.listWidget.clear()
        
    def btnClick_ping(self):
        self.listWidget.addItem("hi")
        
    def btnClick_banner(self):
        self.listWidget.addItem("hi")      
        
    # 스텔스버튼 눌린 경우
    def btnClick_stealth(self):
        try:
            target_ip = self.input_stealth_ip.text()
            target_port = int(self.input_stealth_port.text())
            self.listWidget.addItem(null_scan(target_ip,target_port))
        except:
            
            self.listWidget.addItem("에러")
    #ACK 버튼 누른 경우
    def btnClick_ack(self):
        try:
            target_ip = self.input_ack_ip.text()
            target_port = int(self.input_ack_port.text())
            ack=ack_scan( target_ip,target_port )
            self.listWidget.addItem(ack)
        except:
            self.listWidget.addItem("에러")


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
