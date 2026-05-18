import pygame
import socket 
import time
import cv2
import pickle
import struct
import threading


# Create a socket object 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server_ip='172.24.2.252'

# Define the port to connect to 
server_port = 12345 
 
# Connect to the server 
client_socket.connect((server_ip, server_port)) 

import datetime

running2=True
def videostream():
    data = b""
    payload_size = struct.calcsize("Q")
    recording = False
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    global running2
    while running2:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        cv2.imshow("Receiving...", frame)
        key = cv2.waitKey(1)

        if key == 27:  # Press ESC to stop video capture
            break
        elif key == ord('s'):  # Press 's' to start/stop video recording
            if not recording:
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"recording_{timestamp}.avi"
                out = cv2.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                recording = True
                print(f"Recording started. Output file: {filename}")
            else:
                out.release()
                recording = False
                print("Recording stopped.")

        if recording:
            out.write(frame)

    if out is not None:
        out.release()

    cv2.destroyAllWindows()
    out.release()

        
def goruntu_aldirici():
    pygame.init()
    pygame.joystick.init()
    time.sleep(10)
    print("5 SANIYE BITTI")
    if (pygame.joystick.get_count() == 0):
        print("Joystick bulunamadı")
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        while True:
                # Event işleme
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
            
                    
                  
                pygame.time.wait(15)
                  
                    
                  
        
                button_value = joystick.get_button(1)
                button_value=str(button_value)
                client_socket.send(button_value.encode()) 
                print(button_value)
                if button_value=='1':
                
                    pygame.quit()
                    break

    

def joystick_kontrol():
    pygame.init()
    pygame.joystick.init()
    if (pygame.joystick.get_count() == 0):
        print("Joystick bulunamadı")
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        while True:
                # Event işleme
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
            
                # Eksen değerlerini al
                axis_value1 = joystick.get_axis(0)
                axis_value2 = joystick.get_axis(1)
                axis_value3 = joystick.get_axis(2)
                axis_value4 = joystick.get_axis(3)
                #axis_value5 = joystick.get_axis(4)
                #axis_value6 = joystick.get_axis(5)
            
                dondurulmus_deger1 = str(int((axis_value1 + 30/8)*400))
                dondurulmus_deger2 = str(int((axis_value2 + 30/8)*400))
                dondurulmus_deger3 = str(int((axis_value3 + 30/8)*400))
                dondurulmus_deger4 = str(int((axis_value4 + 30/8)*400))
                #dondurulmus_deger5 = (axis_value5 + 3)*500
                #dondurulmus_deger6 = (axis_value6 + 3)*500
                #client_socket.send(dondurulmus_deger1.encode()) 
        
                print(f"###Eksen 1:\n{dondurulmus_deger1}\n###Eksen2:\n{dondurulmus_deger2}\n###Eksen 3:\n{dondurulmus_deger3}\n###Eksen4:\n{dondurulmus_deger4}\n")
        
                
                dondurulmus_deger1 = str(dondurulmus_deger1)
                client_socket.send(dondurulmus_deger1.encode()) 
                
                dondurulmus_deger2 = str(dondurulmus_deger2)
                client_socket.send(dondurulmus_deger2.encode()) 
        
                dondurulmus_deger3 = str(dondurulmus_deger3)
                client_socket.send(dondurulmus_deger3.encode()) 
        
                dondurulmus_deger4 = str(dondurulmus_deger4)
                client_socket.send(dondurulmus_deger4.encode()) 
        
        
                pygame.time.wait(10)  # CPU kullanımını azaltmak için bir gecikme ekle
                
        
                
        
                button_value = joystick.get_button(0)
                button_value=str(button_value)
                client_socket.send(button_value.encode()) 
                print(button_value)
                if button_value=='1':
                    pygame.quit()
                    break



while 1:
    
    print("1    - Arm - Disarm Check")
    print("2    - Arm Et")
    print("3    - Disarm Et")
    print("4    - Kontrol Fonksiyonu Calistirma")
    print("5    -Goruntu Alma")
    print("6    -Video Streaming Aktif Etme")
    print("100  - Programi Sonlandir\n")

    operasyon = int(input("Hangi Operasyonu Yapmak Istiyorsunuz: "))
    print("deneme3")
    client_socket.send(str(operasyon).encode())
    print("deneme4")

    if(operasyon==4):
        while True:
            girdi = input("Yön Yaz: \nsag - sol - ileri - geri - yukari - asagi - saat_yonu - saat_tersi - stop - joy - pwm\nAna menu icin 'q'\n\n")
            client_socket.send(str(girdi).encode())
            if (girdi == 'q'):
                break
            elif (girdi== "stop2"):
                running2=False
            elif (girdi=="joy"):
                joystick_kontrol()
                girdi== ' '
                
            elif (girdi=="pwm"):
                channel_buffer = int(input("Channel Seciniz: (1-6)\n1:Pitch\n2:Roll\n3:throttle\n4:Yaw\n5:Forward\n6:Lateral\n "))
                pwm_buffer = int(input("PWM degeri belirleyiniz (1000-2000): "))
                client_socket.send(str(channel_buffer).encode())
                client_socket.send(str(pwm_buffer).encode())
    elif (operasyon ==5):
        print("5e girdi")
        goruntu_aldirici()
    elif (operasyon==6):
        threading.Thread(target=videostream).start()