from pymavlink import mavutil

# Подключение к MAVLink
master = mavutil.mavlink_connection('udp:192.168.4.1:14550')

# Ждём HEARTBEAT
print("Ждём HEARTBEAT...")
master.wait_heartbeat()
print("Соединение установлено!")