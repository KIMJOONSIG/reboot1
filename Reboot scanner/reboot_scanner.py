
from os import error
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox,QMainWindow
###########다른 py에서 불러오기

from p1_fin import *
from p1_null import null_scan
from p1_half import half_scan
from xmas import *
from SYNscan import *
from multi_thread_no_port import *
from banner import get_information


##########################################

import concurrent.futures #스레드풀
import threading
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1
from PyQt5 import QtCore

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
form_class = uic.loadUiType(BASE_DIR+r'\scan_design.ui')[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class): 
    def __init__(self): 
        super().__init__() 
        self.setupUi(self)

        ####버튼들 연결
        self.btn_stealth.clicked.connect(self.btnClick_stealth)
       
        self.btn_ping.clicked.connect(self.btnClick_ping)
        
        self.btn_syn.clicked.connect(self.btnClick_syn)

        self.btn_allreset.clicked.connect(self.btnClick_all_reset)

        self.output_ping.setText("")
      
        self.output_stealth.setText("")
        
        self.output_syn.setText("")

        self.btn_ping_reset.clicked.connect(self.btnClick_ping_reset)
      
        self.btn_stealth_reset.clicked.connect(self.btnClick_stealth_reset)
       
        self.btn_syn_reset.clicked.connect(self.btnClick_syn_reset)

    ###쓰레드 만들어두기


    def fin_thread(self, target_ip, target_port):
        result = fin_scan(target_ip, target_port)
        if result is not None:
            self.output_stealth.append(result)
            
        

    def null_thread(self, target_ip, target_port):
        result = null_scan(target_ip, target_port)
        if result is not None:
            self.output_stealth.append(result)
        

    def xmas_thread(self, target_ip, target_port):
        result = xmas_scan(target_ip, target_port)
        if result is not None:
            self.output_stealth.append(result)
        

    def half_thread(self, target_ip, target_port):
        result = half_scan(target_ip, target_port)
        if result is not None:
            self.output_stealth.append(result)

    def syn_thread(self, target_ip, target_port):
        result = syn_scan(target_ip, target_port)
        if result is not None:
            self.output_syn.append(result)
        

    ##버튼이 클릭된 경우들
    def btnClick_all_reset(self):
        self.output_ping.clear()
       
        self.output_stealth.clear()
        
        self.output_syn.clear()

    def btnClick_ping_reset(self):  # type: ignore
        self.output_ping.clear()


    def btnClick_stealth_reset(self):
        self.output_stealth.clear()

    def btnClick_syn_reset(self):
        self.output_syn.clear()

    def btnClick_syn(self):
        target_ip = self.input_syn_ip.text()
        start_port = int(self.syn_start_port.text())
        end_port = int(self.syn_end_port.text())
        try:  
            banner=get_information(target_ip)
            self.output_syn.append(banner)
            with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
                futures = [executor.submit(self.syn_thread, target_ip, port) for port in range(start_port, end_port+1)]
    
        except: 
            
            QMessageBox.information(self, "error", "입력값을 확인해주세요")

    def btnClick_ping(self):
        try:
            target_ip = self.ping_ip.text()
            result = ping_scan(target_ip)
            self.output_ping.append(result)
        except: QMessageBox.information(self, "error", "입력값을 확인해주세요")

   

    # 스텔스버튼 눌린 경우
    def btnClick_stealth(self):
        try:
            
            
            target_ip = self.input_stealth_ip.text()
            start_port = int(self.stealth_start_port.text())
            end_port = int(self.stealth_end_port.text())
            socket.getaddrinfo(target_ip, start_port)#혹시 ip에 오류시 에러 발생시키기 위해
            if end_port - start_port > 1000:
                QMessageBox.information(self, "port", "포트범위를 1000개 이하로 해주세요")

            elif self.combo_stealth.currentText() == "Null Scan":
                threads = []
                for port in range(start_port, end_port+1):
                    thread = threading.Thread(
                        target=self.null_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

            elif self.combo_stealth.currentText() == "Fin Scan":
                threads = []
                for port in range(start_port, end_port+1):
                    thread = threading.Thread(
                        target=self.fin_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            elif self.combo_stealth.currentText() == "Xmas Scan":
                threads = []
                for port in range(start_port, end_port+1):
                    thread = threading.Thread(
                        target=self.xmas_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            else:
                threads = []
                for port in range(start_port, end_port+1):
                    thread = threading.Thread(
                        target=self.half_thread, args=(target_ip, port)
                    )
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

        except:
             QMessageBox.information(self, "error", "입력값을 확인해주세요")


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성

    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
