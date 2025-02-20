import ev3dev.ev3 as ev3 
import socket
import struct
import threading
import time

cs = [ev3.ColorSensor(address='ev3-ports:in1'),ev3.ColorSensor(address='ev3-ports:in2'),ev3.ColorSensor(address='ev3-ports:in3'),ev3.ColorSensor(address='ev3-ports:in4')]
locations = {"none": (0,0), "black": (0,0), "blue" : (0,0),"green": (0,0),"yellow": (0,0),"red": (0,0),"white": (0,0), "brown": (0,0)}
colors = ['none','black','blue','green','yellow','red','white','brown']
colorcount = [[0]*32,[0]*32,[0]*32,[0]*32]
eaten = [0]*4
monitoring = [0]*4
idfile = open("id.txt")
setID = int(idfile.readline().split('\n')[0])
pmscore = 0
inreset = 0
for n in range(0, 4):
   cs[n].mode='COL-AMBIENT'

HOST = '10.42.0.3'    # The remote host
PORT = 5000             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
try: 
   s.connect((HOST, PORT))
   print("connected to "+HOST)
except Exception as e:
   print("server not available" + str(e.args))
   pass
   
class ControlChannel(object):
   global s, colorcount, eaten, monitoring, pmscore
   def __init__(self):
      print ("Active on port: 5000 & 6000")

   def watch(self):
      global s, colorcount, eaten, monitoring, pmscore
      while True:
         data = ''
         try: 
            data_len_str= s.recv( struct.calcsize("!I") )
            data_len = (struct.unpack("!I", data_len_str))[0]
            while (data_len > 0):
               data += s.recv( data_len ).decode()
               data_len -= len(data)
            print(data)
            self.process_msg(data)
         except Exception as e:
            print("FAILURE TO RECV.." + str(e.args) + "..RECONNECTING")
            try:
               s.close()
               s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
               s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
               s.connect((HOST, PORT))
               print("connected to "+HOST)
            except:
               pass
           # threading.Thread(target = self.control,args = (str(msg))).start()

   def process_msg(self, data):
       global s, colorcount, eaten, monitoring, pmscore, inreset
#       print(data)
       if "RESET" in data:
          inreset = 1
          time.sleep(1)
          print("resetting")
          colorcount = [[0]*32,[0]*32,[0]*32,[0]*32]
          eaten = [0]*4
          monitoring = [0]*4
          pmscore = 0
          for n in range(0, 4):
             cs[n].mode='COL-AMBIENT'
          for n in range(0, 4):
              cs[n].mode='COL-REFLECT'
              time.sleep(0.5)
              cs[n].mode='COL-COLOR'
              time.sleep(0.5)
              cs[n].mode='COL-AMBIENT'
              time.sleep(0.5)
              cs[n].mode='COL-REFLECT'
#          print(colorcount)
#          print(eaten)
#          print(monitoring)
          score(1, 1, 'green:(5,2)')
          inreset = 0
#          time.sleep(1)

def score(color, tileID, positionUpdate):
   global pmscore
   global s
   if color == 4:
      if eaten[tileID] != 1:
         pmscore = pmscore #+1 for pacman
      eaten[tileID] = 0 # 1 for pacman

   send_str = (str(pmscore) + ';' + positionUpdate).encode()
   send_msg = struct.pack('!I', len(send_str))
   send_msg += send_str
   print("sending " + str(len(send_str)) + " bytes")
   print("sending total " + str(len(send_msg)) + " bytes")
   print("sending " + str(send_msg))
   try:
      s.sendall(send_msg)
      print("SENDING COMPLETE")
   except Exception as e:
      print("FAILURE TO SEND.." + str(e.args) + "..RECONNECTING")
      try:
         s.close()
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
         s.connect((HOST, PORT))
         print("connected to "+HOST)
         print("sending " + send_msg)
         s.sendall(send_msg)
      except:
         pass


Server = ControlChannel()
threading.Thread(target = Server.watch).start()
score(1, 1, 'green:(5,2)')
print("INIT")

for n in range(0, 4):
   cs[n].mode='COL-REFLECT'

while True:
   try:
      while inreset:
         continue
      for n in range(0, 4):

         # start monitoring if robot is over tile
         if cs[n].mode == 'COL-COLOR':
            if cs[n].value() != 0:
               print( "entering monitoring - color not 0")
               monitoring[n] = 1
         else:
            # reflect mode
            if cs[n].value() > 8:
               monitoring[n] = 1
               print( "entering monitoring - rfl > 8")
               cs[n].mode='COL-COLOR'

         # if we are monitoring then keep stats
         if monitoring[n] == 1:
            valcol = cs[n].value()
            colorcount[n][valcol] = colorcount[n][valcol]+1
            colorcount[n][0] = 0
            colorcount[n][1] = 0
            maxval = max(colorcount[n])
            maxid = colorcount[n].index(maxval)
                           #         print("MAX_COL:"+str(maxid))
                           #         print("TILE NUM:"+str(n+1))
                           #         print("TILE SET:"+str(id))
                           #         print(locations)
            if valcol == 0:
               # robot is no longer on top
               # end monitoring and decide on stats
               locations[colors[maxid]] = (setID-1,n)
               print(colors[maxid]+':'+str(locations[colors[maxid]]))
               score(maxid,n,colors[maxid]+':'+str(locations[colors[maxid]]))
                                   #+":"+str(pmscore))
                                   #            if n+1 == 4:
                                   #               if eaten[counter] != 1:
                                   #                  pmscore = pmscore+1

               # go back to normal mode
               monitoring[n]=0
               if eaten[n] == 1:
                  cs[n].mode='COL-COLOR'
               else:
                  cs[n].mode='COL-REFLECT'
               colorcount[n] = [0]*8
                              #      colorcount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

   except Exception as e:
      print(str(e.args))
      pass
        #s.close()
