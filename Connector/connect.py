import socket
import serial
import serial.tools.list_ports
import time
from pymavlink import mavutil

# Настройки
UDP_PORT = 14550  # Порт для приема сообщений от автопилота

def discover_via_udp():
    print("Searching for autopilot via UDP...")
    # Создаем сокет для прослушивания
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))

    sock.settimeout(5)  # Устанавливаем таймаут для ожидания сообщений
    try:
        while True:
            data, addr = sock.recvfrom(1024)  # Получение данных
            print(f"UDP Autopilot found: IP={addr[0]}, PORT={addr[1]}")
            return 'UDP', addr[0], addr[1]
    except socket.timeout:
        print("No UDP autopilot found")
    finally:
        sock.close()

    return None, None, None

def discover_via_usb():
    # Получение списка всех доступных последовательных портов
    ports = serial.tools.list_ports.comports()
    for port in ports:
        try:
            print(f"Trying USB port: {port.device}")
            # Попытка открыть последовательный порт
            with serial.Serial(port.device, 57600, timeout=1) as ser:
                # Попытка отправить команду HEARTBEAT
                master = mavutil.mavlink_connection(port.device)
                master.wait_heartbeat()
                print(f"USB Autopilot found: {port.device}")
                return 'USB', port.device, None
        except (serial.SerialException, Exception) as e:
            print(f"Failed to connect to {port.device}: {e}")

    return None, None, None

if __name__ == "__main__":
    # Попытка обнаружения через UDP
    connection_type, address, port = discover_via_udp()
    if connection_type:
        print(f"Connection Type: {connection_type}, IP: {address}, PORT: {port}")
    else:
        # Если не найдено через UDP, пробуем USB
        connection_type, address, port = discover_via_usb()
        if connection_type:
            print(f"Connection Type: {connection_type}, Device: {address}")
        else:
            print("No autopilot found via UDP or USB.")