import serial
import mysql.connector
import time
from decimal import Decimal

cnx = mysql.connector.connect(user='root', password='lcm5613176',
                              host='127.0.0.1',
                              database='SenseData',
                              )


def add_data(time, temperature, humidity):
    cursor = cnx.cursor()
    query = ("INSERT INTO sensedata "
             "(time, temperature, humidity) "
             "VALUES (%s, %s, %s)")
    data = (time, temperature, humidity)

    cursor.execute(query, data)
    cnx.commit()

    cursor.close()


def get_time():
    ticks = time.time()
    cur_time = str(int(ticks))[5:]
    cur_time = int(cur_time)
    return cur_time


def parse_data(data):
    """
    :param data:
    :return time, temperature, humidity:
    data = 02390108
    湿度 = （（0x02 * 256) + 0x39) /10 = 56.9%RH
    温度 = （（0x01 * 256) + 0x08) /10 = 26.4℃
    """
    humi_high = data[0:-6]
    humi_low = data[2:-4]
    temp_high = data[4:-2]
    temp_low = data[6:]
    temperature = ((int(temp_high, 16) * 256) + int(temp_low, 16)) / 10
    humidity = ((int(humi_high, 16) * 256) + int(humi_low, 16)) / 10

    temperature = Decimal(str(temperature)).quantize(Decimal('0.0'))
    humidity = Decimal(str(humidity)).quantize(Decimal('0.0'))

    cur_time = get_time()

    return cur_time, temperature, humidity


def main():

    s = serial.Serial('com3', 9600)
    #s.open()
    while(True):
        # request for a sensor data
        d = bytes.fromhex('01 03 00 14 00 02 84 0f')
        """发送RTU帧格式数据“01 03 00 14 00 02 84 0f”给协调器"""
        s.write(d)
        # receive data from cc2530
        n = s.inWaiting()
        if n:
            data = str(s.read(n))[6:-4]
            """收到传感器的16进制数010304 02390108 2BD0"""
            """02 39：湿度数据"""
            """01 08：温度数据"""
            # print(data)
            Time, tempe, humi = parse_data(data)

            add_data(Time, tempe, humi)
        time.sleep(2)

    s.close()
    cnx.close()


if __name__ == '__main__':
    main()
