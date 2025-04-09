from pymavlink import mavutil
import time

connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

print("Ожидание сообщения HEARTBEAT...")
connection.wait_heartbeat()
print("Соединение установлено с системой:", connection.target_system)

for i in range(10):
    print(i)
    time.sleep(1)