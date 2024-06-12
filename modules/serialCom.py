import serial

def serialCall() :
    serial_com = False
    try :
        ser = serial.Serial('COM3', 9600)
        ser.flushInput()
        password_return = 0
        print('Working Live')
        working = True
        while working :
            ser_bytes = ser.readline()
            decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            if decoded_bytes == '123456':
                password_return = 1
                print('Password Matched')
                serial_com = True
                working = False
            else :
                print('Please give the correct password!')

    except:
        print('serial Com not available, going to direct input')