Light Sensor Monitor

A Raspberry Pi script that reads ambient light levels from a TSL2591 lux sensor and reports them to a Blynk dashboard, with a notification triggered if a light source is detected while the room is dark. 
The Rpi is controlled remotely with a headless setup (ssh connection). Tmux is used to create a virtual terminal that runs independently from the ssh connection. Even when the connection is terminated, the sensor keeps providing measurements, as long as the client (Rpi5) stays online. 

Credit
TSL2591 driver from Waveshare's TSL2591X-Light-Sensor.
