import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from NULLscan import *
from p1_ack import *
from p1_fin import *
from xmas import *

import subprocess
import time
import threading
from multi_thread_no_port import *
from PyQt5 import QtCore

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
        self.textBrowser.setText("")

    ###쓰레드 만들어두기
    def ack_thread(self, target_ip, target_port):
        result = ack_scan(target_ip, target_port)
        self.textBrowser.append(result)

    def fin_thread(self, target_ip, target_port):
        result = fin_scan(target_ip, target_port)
        self.textBrowser.append(result)

    def null_thread(self, target_ip, target_port):
        result = null_scan(target_ip, target_port)
        self.textBrowser.append(result)

    def xmas_thread(self, target_ip, target_port):
        result = xmas_scan(target_ip, target_port)
        self.textBrowser.append(result)

    def half_thread(self, target_ip, target_port):
        result = ack_scan(target_ip, target_port)
        self.textBrowser.append(result)










##버튼이 클릭된 경우들
    def btnClick_reset(self):
        self.textBrowser.clear()
        self.textBrowser2.clear()


    def btnClick_ping(self):
        target_ip=self.ping_ip.text()
        result = ping_scan(target_ip)
        self.textBrowser.append(result)

    def btnClick_banner(self):
        self.listWidget.addItem("hi")
        
    
    
    

    # 스텔스버튼 눌린 경우
    def btnClick_stealth(self):
        try:
            target_ip = self.input_ack_ip.text()
            start_port = int(self.stealth_start_port.text())
            end_port = int(self.stealth_end_port.text())
            if self.combo_stealth.currentText() == "Null Scan":
                threads = []
                for port in range(start_port, end_port):
                    thread = threading.Thread(
                        target=self.ack_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
                    
            elif self.combo_stealth.currentText() == "Fin Scan":
                threads = []
                for port in range(start_port, end_port):
                    thread = threading.Thread(
                        target=self.fin_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            elif self.combo_stealth.currentText() == "Xmas Scan":
                threads = []
                for port in range(start_port, end_port):
                    thread = threading.Thread(
                        target=self.xmas_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            else:
                self.textBrowser2.setText("아직 준비가 덜되었어요")
                

        except:
            self.textBrowser.setText("error가 발생했습니다")

    # ACK 버튼 누른 경우
    def btnClick_ack(self):
        try:
            target_ip = self.input_ack_ip.text()
            start_port = int(self.ack_start_port.text())
            end_port = int(self.ack_end_port.text())

            self.textBrowser.setText("start")
            word = ""

            threads = []
            for port in range(start_port, end_port):
                thread = threading.Thread(
                    target=self.ack_thread, args=(target_ip, port)
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        except:
            self.textBrowser.setText("error가 발생했습니다")


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성

    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
