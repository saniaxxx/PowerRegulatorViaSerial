
# -*- coding: utf-8 -*-
import logging
import os
import serial
from subprocess import Popen
from cbpi.api import *

logger = logging.getLogger(__name__)

def getSerialDevices():
    try:
        arr = []
        for dirname in os.listdir('/dev'):
            if dirname.startswith("ttyUSB"):
                arr.append(dirname)
        return arr
    except:
        return []

@parameters([Property.Select(label="Port", options=getSerialDevices()),
            Property.Select(label="Baudrate", options=[9600, 19200, 57600, 115200]),
            Property.Number(label="MaxPower", configurable = True, default_value = 3000, description="Maximum Heater Power, Wt")])
class SerialPortPowerRegulator(CBPiActor):
    @action("Set Power", parameters=[Property.Number("Power", configurable=True)])
    async def action(self, **kwargs):
        print("Set Power Triggered", kwargs)
        power = max(0, min(100, int(kwargs["Power"])))
        if power > 0:
            await self.on(power=power)
        else:
            await self.off()

    def __init__(self, cbpi, id, props):
        super().__init__(cbpi, id, props)
        self.power = 100 * int(self.state)

    async def start(self):
        await super().start()
        self.port = self.props.get("Port", "")
        self.baudrate = int(self.props.get("Baudrate", 9600))
        self.max_power = int(self.props.get("MaxPower", 1000))
        try:
            self.serial = serial.Serial(
                port=f"/dev/{self.port}",
                baudrate = self.baudrate,
                timeout=1
            )
            p = Popen(['stty', '-F', f'/dev/{self.port}', '-hupcl'])
            p.terminate()
        except Exception as e:
            print(e)

    async def on(self, power=100):
        self.power = power
        self.state = True
        await self.cbpi.actor.actor_update(self.id, self.power)
        logger.info("ACTOR %s ON" % self.id)
        logger.info("ACTOR POWER IS %d" % power)
        try:
            watt = int(self.max_power / 100.0 * power)
            self.serial.write(str.encode(f"TW{watt}\n"))
        except Exception as e:
            print(e)

    async def off(self):
        self.power = 0
        self.state = False
        await self.cbpi.actor.actor_update(self.id, self.power)
        logger.info("ACTOR %s OFF " % self.id)
        try:
            self.serial.write(b"TW0\n")
        except Exception as e:
            print(e)

    def get_state(self):
        return self.state

    def get_power(self):
        return self.power

    def to_dict(self):
        try:
            return dict(id=self.id, name=self.name, type=self.type, props=self.props.to_dict(), state2="HELLO WORLD", state=self.instance.get_state())
        except Exception as e:
            print(e)


def setup(cbpi):
    cbpi.plugin.register("SerialPortPowerRegulator", SerialPortPowerRegulator)
