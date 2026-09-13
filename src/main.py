import logging

from hardware.TSL2591 import TSL2591

FORMAT = "%(asctime)s,%(levelname)s %(name)s - %(message)s"
logging.basicConfig(filename="light_sensor.log", level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger("main.py")


def main():
    light_sensor = TSL2591()

    logger.info("Light Sensor Initialised. Main Loop Starts.")
    light_sensor.loop()


if __name__ == "__main__":
    main()
