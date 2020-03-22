import pexpect
import time
from time import strftime
import sys
import os
import datetime

def hexStrToInt(hexstr):
    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val

child = pexpect.spawn("gatttool -b 24:71:89:07:2D:82 --interactive")

print("Connecting to:"),
NOF_REMAINING_RETRY = 3
while True:
  try:
    child.sendline("connect")
    child.expect("Connection successful", timeout=5)
  except pexpect.TIMEOUT:
    NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
    if (NOF_REMAINING_RETRY>0):
      print( "timeout, retry...")
      continue
    else:
      print ("timeout, giving up.")
      break
  else:
    print("Connected!")
    break
if NOF_REMAINING_RETRY>0:

  #child.sendline("char-write-cmd 0x24 01")
  # open file
  file = open("readings_collected.csv", "a")
  if (os.path.getsize("readings_collected.csv")==0):
    file.write("\ttime\tTemperature\tAmbient light\tPressure\tHumidity\n")

  #file.write("1")
  #file.write("\t")
  #file.write(str(unixTime)) # Unix timestamp in seconds
  #file.write("\t")

  child.sendline("char-write-cmd 0x24 01")
  child.expect("\r\n", timeout=60)
  time.sleep(1)

  child.sendline("char-write-cmd 0x44 01")
  child.expect("\r\n", timeout=60)
  time.sleep(1)

  child.sendline("char-write-cmd 0x34 01")
  child.expect("\r\n", timeout=60)
  time.sleep(1)

  child.sendline("char-write-cmd 0x2C 01")
  child.expect("\r\n", timeout=60)
  time.sleep(1)
  counter = 1
  while True:
      oneRow = ""
      unixTime = int(time.time())
      unixTime += 60*60 # GMT+1
      unixTime += 60*60 # added daylight saving time of one hour

      oneRow = oneRow + str(counter) +"\t"
      oneRow = oneRow + strftime("%Y-%m-%d %H:%M:%S")+"\t"
      #oneRow = oneRow + str(unixTime)+","
      counter = counter + 1
        # Temperature (0x2018)


      child.sendline("char-read-hnd 0x21")
      child.expect("Characteristic value/descriptor: ", timeout=60)
      child.expect("\r\n", timeout=60)
      print("Temperature:  "),
      print(child.before),
      print(float(hexStrToInt(child.before[0:5]))/100)
      #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      oneRow = oneRow + str(float(hexStrToInt(child.before[0:5]))/100) +"\t"

      #file.write("\t")
    # Humidity (0x2018)
  #while True:

      child.sendline("char-read-hnd 0x41")
      child.expect("Characteristic value/descriptor: ", timeout=60)
      child.expect("\r\n", timeout=60)
      print("Ambient Light:  "),
      print(child.before),
      print(float(hexStrToInt(child.before[0:5]))/100)
      #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      oneRow = oneRow + str(float(hexStrToInt(child.before[0:5]))/100) +"\t"


      child.sendline("char-read-hnd 0x31")
      child.expect("Characteristic value/descriptor: ", timeout=60)
      child.expect("\r\n", timeout=60)
      print("Pressure:  "),
      print(child.before),
      print(float(hexStrToInt(child.before[0:5]))/100)
      #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      oneRow = oneRow + str(float(hexStrToInt(child.before[0:5]))/100) +"\t"



      child.sendline("char-read-hnd 0x29")
      child.expect("Characteristic value/descriptor: ", timeout=60)
      child.expect("\r\n", timeout=60)
      print("Humidity:  "),
      print(child.before),
      print(float(hexStrToInt(child.before[0:5]))/100)
      oneRow = oneRow + str(float(hexStrToInt(child.before[0:5]))/100) +"\t"
      #file.write(str(float(hexStrToInt(child.before[0:5]))/100))
      #file.write("\t")
      oneRow = oneRow + "\n"
      #print("I will write this stuff ->", oneRow)
      file.write(oneRow)
      time.sleep(60)


  file.close()
  print("done!")
  sys.exit(0)
else:
  print("FAILED!")
  sys.exit(-1)

