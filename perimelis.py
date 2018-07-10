import  sys, time
import  threading
import  colorama

from    colorama import init, Fore, Back, Style
from    socket import *


BUFSIZE         = 65536 *32
testdata        = 'x'   *65536 *4
FINAL_RESULTS   = Fore.YELLOW
SUCCESS         = Fore.GREEN
FAIL            = Fore.RED
bw_port     = 6000

class ThreadScanHosts(threading.Thread):
    
    def __init__(self, dur, sockett, SendorReceive):
        threading.Thread.__init__(self)
        self.RTsocket       = sockett
        self.SendOrReceive  = SendorReceive
        self.duration = dur
    
    def run(self):
        if self.SendOrReceive == "send":
            self.sendData(self.RTsocket)
        elif self.SendOrReceive == "receive":
            self.receiveData(self.RTsocket)

    def sendData(self,socket_):
            totaldata=0
            tempdata = 0
            sure=time.time()
            temp = time.time()
            xx=bytearray(testdata,"utf-8")
            sys.stdout.write("Sending proccess is starting..." + "\n")
            while 1: 
                try:
                    sended = socket_.send(xx)
                    totaldata   = totaldata + sended
                    now=time.time()
                    if now-temp >1:
                        sys.stdout.write("[-][Sent] Packets :" +str(totaldata-tempdata) + "\tBandwidth: "+str(round((totaldata-tempdata)*0.001*0.001*8/ (now-temp),2)) + " Mbps" + '\n')
                        temp = time.time()
                        tempdata=totaldata
                    if now-sure > self.duration:
                        end = time.time()
                        sys.stdout.write(FINAL_RESULTS+"[*][Sent] Packets :" +str(totaldata) + "\tBandwidth: "+str(round(totaldata*0.001*0.001*8/ (end-sure),2)) + " Mbps" + "\n")
                        
                        return (sended/(end-sure))
                except:
                    end = time.time()
                    sys.stdout.write(FINAL_RESULTS+"[*][Sent] Packets :" +str(totaldata) + "\tBandwidth: "+str(round(totaldata*0.001*0.001*8/ (end-sure),2)) + " Mbps" + "\n")
                    return (sended/(end-sure))
                        
    def receiveData(self,socket_):
        totaldata = 0
        tempdata=0
        maxlen=0
        end=time.time()
        once = time.time()
        temp=time.time()
        socket_.settimeout(1)
        sys.stdout.write("Receiving proccess is starting..." + "\n")
        
        while 1:          
            try:
                rubbish1=time.time()
                data = socket_.recv(BUFSIZE)
                totaldata += len(data)
                n=len(data)
                if n>maxlen:
                    maxlen=n
                if not data:    
                    end = time.time()
                    socket_.shutdown(0)
                    sys.stdout.write(FINAL_RESULTS+"[*][Recv] Packets :" +str(totaldata) + "\tBandwidth: "+str(round(totaldata*0.001*0.001*8/ (end-once),2)) + " Mbps" + "\n")
                    sys.stdout.write(FINAL_RESULTS+"[*] Maximum Length of received data: "+str(maxlen) + "\n")
                    return (end-once)
                
                now=time.time()
                if (now-temp) >1:
                    sys.stdout.write("[-][Recv] Packets :" +str(totaldata-tempdata) + "\tBandwidth: "+str(round((totaldata-tempdata)*0.001*0.001*8/ (now-temp),2)) + " Mbps" + "\n")
                    
                    temp=time.time()
                    tempdata = totaldata
                
            except :
                socket_.close()
                sys.stdout.write(FINAL_RESULTS+"[*][Recv] Packets :" +str(totaldata) + "\tBandwidth: "+str(round(totaldata*0.001*0.001*8/ (rubbish1-once),2)) + " Mbps" + "\n")
                sys.stdout.write(FINAL_RESULTS+"[*] Maximum Length of received data: "+str(maxlen) + "\n")
                
                return (rubbish1-once)
            
def client():
 
    ip          = input("Target (server side) IP-Address: ")
    duration    = 15
    BaseSocket   = socket(AF_INET, SOCK_STREAM)
    BaseSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        BaseSocket.connect((ip, int(bw_port)))
        print(SUCCESS+"Client is connected to Bandwidth-Server.")
    except:
        print(FAIL+"Client could not connect to Bandwidth-Server.")
        sys.exit()
    
    recv_thread = ThreadScanHosts(duration, BaseSocket, "receive") 
    send_thread = ThreadScanHosts(duration, BaseSocket, "send") 
    recv_thread.start() 
    send_thread.start()   
    send_thread.join()
    recv_thread.join()
    
    print(SUCCESS+"Test Operation has done.")

def server():

    localsocket = socket(AF_INET, SOCK_DGRAM)
    localsocket.connect(("8.8.8.8", 80))
    localIP=(localsocket.getsockname()[0])
    localsocket.close()
    server_IP = localIP
    duration = 15

    BaseSocket = socket(AF_INET, SOCK_STREAM)
    BaseSocket.  setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    BaseSocket.  bind((server_IP, int(bw_port)))
    BaseSocket.  listen(1)
    
    try:
        BaseConn, (clientAddress_Base, clientPort_Base) = BaseSocket.accept()
        print(SUCCESS+"Server accepted Bandwidth-Client.")
    except:
        print(FAIL+"Server coluld not accept Bandwidth-Client.")
        sys.exit()

    recv_thread = ThreadScanHosts(duration, BaseConn, "receive")
    send_thread = ThreadScanHosts(duration, BaseConn, "send") 
    recv_thread.start()   
    send_thread.start()   
    send_thread.join()
    recv_thread.join()
   


    print(SUCCESS+"Test Operation has done.")

def usage():
    print("[*] py [FILENAME] -s | -c")

if __name__=="__main__":
    init()                  # FOR COLORAMA ON WINDOWS PLATFORMS
    init(autoreset=True)    # AUTORESET COLORING
    opt = sys.argv[1]
    
    print("\n[*] BANDWITH TEST\n")
    print("[*] Please do not run any program during the test")

    if len(sys.argv)!=2:
        usage()
        sys.exit()
    if opt == "-s":
        server()
    elif opt == "-c":
        client()
    else:
        print("[*] Wrong Choose!")
        usage()
        sys.exit()

