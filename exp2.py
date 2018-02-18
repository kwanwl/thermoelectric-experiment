__author__ = 'xx'
import time
import numpy as np
import Gnuplot
#import scipy
#from scipy import io
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import visa
import serial
import sys
from serial.tools import list_ports

rm = visa.ResourceManager()
usb_ports = rm.list_resources()
f = open("exp2_ver2.txt","w")
#print usb_ports[0]
#print usb_ports[1]
#print len(usb_ports)

print ('hello physical world\n')
ports = list_ports.comports()

#print ports

tmser = 99
#tm = 99
ps = 99

#print len(ports)
for y in range(0, len(ports)):
    if 'COM' in ports[y][0]:
        #print ports[y][0]
        ser_tm = serial.Serial(ports[y][0], timeout=1)
        ser_tm.flushInput()
        s = ser_tm.read(16)
        #print s
        #print len(s)
        if len(s) == 16:
            tmser = y
#        elif len(s) == 0:
#            ps = y




#print ('PS port ='),
#print ports[ps][0]

ser_tm.close()
if tmser == 99:
    print 'please connect thermocouple reader'
    sys.exit(1)
ser_tm = serial.Serial(ports[tmser][0])

for y in range(0, len(usb_ports)):
    if 'INSTR' and 'USB' in usb_ports[y]:
        #print usb_ports[y]
        usb_ps = rm.open_resource(usb_ports[y],open_timeout=1000)
        ps=y
#    if 'ASRL' in usb_ports[y]:
#        print usb_ports[y]
#        usb_tm = rm.open_resource(usb_ports[y],open_timeout=0)
#        usb_tm.
#        tm=y


if ps==99:
    print 'please connect power supply'
    sys.exit(2)

#print ('TM port ='),
#print ports[tmser][0]
print ('TM port ='),
print ports[tmser][0]
print ('PS port ='),
print usb_ports[ps]
print usb_ps.query('*IDN?')


usb_ps.write('*CLS')
usb_ps.write('VOLT:LEV 3V')
usb_ps.write('CURR:LEV 2A')
usb_ps.write('OUTP:STAT ON')
time.sleep(0.5)

time.sleep(0.5)
ser_tm.flushInput()
print ('Experiment 2: Stage 1')
f.write('Experiment 2: Stage 1\n')
print ('Voltage Applied = 3.0V')
print ('time(s)\tCH1(C)\tCH2(c)\t Current(A)')
f.write ('time(s)\tCH1(C)\tCH2(c)\t Current(A)\n')


ti = []
ch1 = []
ch2 = []
flag1 = 0
flag2 = 0
flag3 = 0
while flag1 == 0:
    s = ser_tm.read(16)
    if s[2] == '4':
        flag1 = 1
while flag3==0:
#for z in range(0, 60):
    current = usb_ps.query("MEAS:CURR:DC?")
    for x in range(0,4):
        fs=0
        ser_tm.flushInput()
        s = ser_tm.read(16)
        if s[14].isdigit():
            fs=float(s[12:15])
            fw=fs/10

        if s[2] == '1':
            if flag2 == 0:
                t = time.time()
                flag2 = 1
            tnow = time.time() - t
            print '{0:.1f}'.format(tnow), '\t',
            f.write('{0:.1f}'.format(tnow))
            f.write('\t')
            print fs/10, '\t',
            f.write(str(fw))
            f.write('\t')
            ti.append(tnow)
            ch1.append(fw)


        if s[2] == '2':
            print fs/10, '\t',
            f.write(str(fw))
            f.write('\t')
            ch2.append(fw)
        #if s[2] == '3':
        #    print fs/10, '\t',
        #if s[2] == '4':
        #    print fs/10, '\t',
    print current,
    f.write(current)

#    f.write('\n')
    if tnow>59:
        flag3=1
flag2 = 0
flag3 = 0
print '\n'
print 'Flip the toggle switch\n'

usb_ps.write('CURR:LEV 0A')
usb_ps.write('VOLT:LEV 3V')



for z in range(0,2,1):
    time.sleep(1)
    print ('{:d}'.format(2-z))

print('Stage 2')
f.write('Stage 2\n')
print('discharging...')




print ('time(s)\tCH1(C)\tCH2(C)\t Voltage(V)')
f.write ('time(s)\tCH1(C)\tCH2(C)\t Voltage(V)\n')

while flag3==0:
#for z in range(0, 60):


    voltage = usb_ps.query("MEAS:VOLT:DC?")
    for x in range(0,4):
        fs=0
        ser_tm.flushInput()

        s = ser_tm.read(16)
        if s[14].isdigit():
            fs=float(s[12:15])
            fw=fs/10
        if s[2] == '1':
            if flag2 == 0:
                #t = time.time()
                flag2 = 1
            tnow = time.time() - t
            print '{0:.1f}'.format(tnow), '\t',
            f.write ('{0:.1f}'.format(tnow))
            f.write('\t')
            print fs/10, '\t',
            f.write(str(fw))
            f.write('\t')
            ti.append(tnow)
            ch1.append(fw)
        if s[2] == '2':
            print fs/10, '\t',
            f.write(str(fw))
            f.write('\t')
            ch2.append(fw)
        #if s[2] == '3':
        #    print fs/10, '\t',
        #if s[2] == '4':
        #    print fs/10, '\t',
    print voltage,
    f.write(voltage)
#    f.write('\n')

    if float(voltage)<0.01:
        flag3=1

print 'end of experiment 2'
f.write('end of experiment 2')
#time.sleep(1)
usb_ps.write("OUTP:STAT OFF")
usb_ps.close()

ser_tm.close()
f.close()
#print ti
#print ch1
#print ch2

ti_a=np.asarray(ti)
ch1_a=np.asarray(ch1)
ch2_a=np.asarray(ch2)
#print ti_a
#print ch1_a

plt.plot(ti_a,ch1_a,'r-', ti_a,ch2_a, 'b-')
plt.xlabel('Time(s)')
plt.ylabel('Temperature(C)')
plt.legend(('Channel 1','Channel 2'),loc='upper right')
plt.title('Experiment 2')
plt.show()

