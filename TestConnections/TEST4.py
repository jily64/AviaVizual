import serial.tools.list_ports
from pymavlink import mavutil
import socket

def find_serial_device():
    """
    Функция для поиска MAVLink-устройства через последовательные порты.
    """
    print("Сканирую последовательные порты...")
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            # Пытаемся подключиться к устройству
            connection = mavutil.mavlink_connection(port.device, baud=115200, timeout=2)
            if connection:
                print(f"Устройство MAVLink найдено на порту {port.device}")
                return connection
        except Exception as e:
            pass
    return None

def find_wifi_device(ip="127.0.0.1", port=14550):
    """
    Функция для проверки подключения MAVLink-устройства через Wi-Fi.
    """
    try:
        # Проверяем, доступен ли сокет
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.close()
        # Если сокет доступен, создаем MAVLink-соединение
        connection = mavutil.mavlink_connection(f"udp:{ip}:{port}")
        heartbeat = connection.recv_match(type='HEARTBEAT', blocking=True, timeout=5)
        print(heartbeat)
        print(f"Устройство MAVLink найдено по Wi-Fi: {ip}:{port}")
        return connection
    except Exception as e:
        pass
    return None

def main():
    """
    Основная функция для автоматического определения подключения MAVLink-устройства.
    """
    print("Ищу MAVLink-устройство...")
    
    # Сначала проверяем последовательные порты
    serial_connection = find_serial_device()
    if serial_connection:
        print("Соединение установлено через последовательный порт!")
        return serial_connection

    # Если не найдено, пробуем подключение по Wi-Fi
    wifi_connection = find_wifi_device()
    if wifi_connection:
        print("Соединение установлено через Wi-Fi!")
        return wifi_connection

    print("Не удалось найти MAVLink-устройство. Проверьте подключение.")
    return None

if __name__ == "__main__":
    connection = main()
    message = ""
    if connection:
        message = "Готов к работе с MAVLink-устройством! 4"
    else:
        message = "Подключение не удалось. 4"
    
    with open("DebugLog", "+a") as f:
        f.write(message + "\n")

    
