from pymavlink import mavutil

port = "/dev/ttyACM0"
baudrate = 115200

print(f"Подключение к {port}...")
connection = mavutil.mavlink_connection(port, baud=baudrate)

print("Ожидание HEARTBEAT...")
connection.wait_heartbeat()
print("HEARTBEAT получен! Соединение установлено.")

print(f"Система: {connection.target_system}, Компонент: {connection.target_component}")