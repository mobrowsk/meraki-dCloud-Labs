import testInflux
import testMeraki
import time

#Initialize Classes
IDB = testInflux.InfluxDB()
M = testMeraki.Meraki()

def update_deviceAvailabilities():
    orgs_list = ['215332', '351024', '351028', '622622648483971160', '622622648483971212', '660903245316620327','660903245316620328']
    json_data = M.get_meraki_device_availabilities(orgs_list)
    IDB.writeDevicestoDB(json_data)
    print("Success")

interval = 300 #5 minute timer
while True:
    update_deviceAvailabilities()
    time.sleep(interval)