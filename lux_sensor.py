"""
Script for automating LUX measurements in an indoor environment. 
- Smoothened measurements provided every 60s
- Notification sent if light is opened while in darkness
"""

import time
import sys
import os
import requests
import logging
import TSL2591

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# suppress unwanted  info from TSL module 
logging.basicConfig(level=logging.INFO)

sensor = TSL2591.TSL2591()
# sensor.SET_InterruptThreshold(0xff00, 0x0010)

try:
    lux = sensor.Lux
    print('Lux: %d'%lux)
    requests.get(f"https://blynk.cloud/external/api/update?token=R3K5bjsV7EmX625W4h5rQi7JeNfsImBT&V0={lux}")
    prev_avg = 0 
    while True:
        
        count   = 0.0 
        sent    = False
        for _ in range(60):
            
            lux = sensor.Lux
            print('Lux: %d'%lux)
            sensor.TSL2591_SET_LuxInterrupt(50, 200)
            
            if lux >= 20 and prev_avg < 10 : 
                """
                - avg lux < 10 when room is dark
                - lux spike when dark indicates a presence of light source in the room 
                """
                # short confirmation
                lux = sensor.Lux
                print('Lux: %d'%lux)
                sensor.TSL2591_SET_LuxInterrupt(50, 200)

                if lux > 20 and prev_avg < 10 and not sent: 
                    # Send a notification if not already sent one during the 60s of this loop
                    r = requests.get(
                        "https://blynk.cloud/external/api/logEvent",
                        params={
                            "token": "R3K5bjsV7EmX625W4h5rQi7JeNfsImBT",
                            "code": "detected_light",
                            "description": "Μήπως άνοιξες το φως; Τσέκαρέ το"
                        }
                    )
                    print(r.status_code, r.text)
                    sent = True

            """infrared = sensor.Read_Infrared
            print('Infrared light: %d'%infrared)
            visible = sensor.Read_Visible
            print('Visible light: %d'%visible)
            full_spectrum = sensor.Read_FullSpectrum
            print('Full spectrum (IR + visible) light: %d\r\n'%lux)"""
            count += lux
            time.sleep(1)
        
        avg = int(count/60)
        requests.get(f"https://blynk.cloud/external/api/update?token=R3K5bjsV7EmX625W4h5rQi7JeNfsImBT&V0={avg}")
        prev_avg = avg
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    sensor.Disable()
    exit()

