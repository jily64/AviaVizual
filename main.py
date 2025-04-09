from Modules import TimeHead
import time 


time_hd = TimeHead.TimeHead("app")

time_hd.set_zone(2, 1, "m")
time_hd.set_active()
print(time_hd.zones[2])

while True:
    time_hd.update()
    print(time_hd.is_active, time_hd.active_zone)
    time.sleep(0.5)