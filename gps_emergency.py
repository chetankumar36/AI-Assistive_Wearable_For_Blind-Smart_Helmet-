import threading
import serial
from time import sleep
import time
from gpiozero import Button
import time
from email.message import EmailMessage
import smtplib
from gpiozero import Buzzer

buzzer = Buzzer(20)
button = Button(21)

ser = serial.Serial ("/dev/serial0",9600)
ser.flushInput()
gpgga_info = "$GPGGA," #before it was gngga
GPGGA_buffer = 0
NMEA_buff = 0
lat = 0
longi = 0

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position

def gps():
    global lat,longi
    while True:
        print("Running")
        received_data = (str)(ser.readline()) #read NMEA string received
        print(received_data)

        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after “$GPGGA,” string
            NMEA_buff = (GPGGA_buffer.split(','))
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            print("NMEA Time: ", nmea_time,'\n')
            try:
                
                lat = (float)(nmea_latitude)
                lat = convert_to_degrees(lat)
                longi = (float)(nmea_longitude)
                longi = convert_to_degrees(longi)
                print ("NMEA Latitude:", lat,"NMEA Longitude:", longi,'\n')
            except:
                print("Gps not connected")
            # print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')

        sleep(0.5)
def email(message):
    buzzer.on()
    Sender_Email = "chetannaikchetan866@gmail.com"
    Reciever_Email = "chetannaikchetan8@gmail.com"
    Password = "mavyropagszncqit"
    newMessage = EmailMessage()
    newMessage['Subject'] = "Alert"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    newMessage.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)
    print("mail Sent")
    buzzer.off()

def button_check():
    global lat,longi
    while True:
        if button.is_pressed:
            print("Emergency Button pressed")
            print("lat is: ", lat)
            print("longi is: ", longi)
            if(longi==0):
                lat = 13.966325221954305
                longi=75.57947000567557
            content = "emergency button is pressed at the location http://maps.google.com/?q=" + str(lat) + ',' + str(longi)
            email(content)
            time.sleep(1)
        time.sleep(0.1)


if __name__ == '__main__':
    t1 = threading.Thread(target=gps)
    t2 = threading.Thread(target=button_check)

    t1.start()
    t2.start()

    t1.join()
    t2.join()