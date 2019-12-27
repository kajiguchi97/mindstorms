# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.

import time
import logging
import json
import random
import threading

from enum import Enum
from agt import AlexaGadget

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, MediumMotor, LargeMotor

# Set the logging level to INFO to see messages from AlexaGadget
logging.basicConfig(level=logging.INFO)

class Command(Enum):
    """
    The list of preset commands and their invocation variation.
    These variations correspond to the skill slot values.
    """

    RIGHT = ['right']
    LEFT = ['left']
    GO = ['go']
    STRAIGHT = ['straight']
    READY = ['ready']


class MindstormsGadget(AlexaGadget):
    """
    A Mindstorms gadget that performs movement based on voice commands.
    Two types of commands are supported, directional movement and preset.
    """

    def __init__(self):
        """
        Performs Alexa Gadget initialization routines and ev3dev resource allocation.
        """
        super().__init__()

        # Ev3dev initialization
        self.leds = Leds()
        self.sound = Sound()
        self.wrist = MediumMotor(OUTPUT_A)
        self.elbow = LargeMotor(OUTPUT_B)
        self.shoulder = LargeMotor(OUTPUT_C)
        self.shoulder.reset()


    def on_connected(self, device_addr):
        """
        Gadget connected to the paired Echo device.
        :param device_addr: the address of the device we connected to
        """
        self.leds.set_color("LEFT", "GREEN")
        self.leds.set_color("RIGHT", "GREEN")
        print("{} connected to Echo device".format(self.friendly_name))

    def on_disconnected(self, device_addr):
        """
        Gadget disconnected from the paired Echo device.
        :param device_addr: the address of the device we disconnected from
        """
        self.leds.set_color("LEFT", "BLACK")
        self.leds.set_color("RIGHT", "BLACK")
        print("{} disconnected from Echo device".format(self.friendly_name))

    def on_custom_mindstorms_gadget_control(self, directive):
        """
        Handles the Custom.Mindstorms.Gadget control directive.
        :param directive: the custom directive with the matching namespace and name
        """
        try:
            payload = json.loads(directive.payload.decode("utf-8"))
            print("Control payload: {}".format(payload))
            control_type = payload["type"]

            if control_type == "command":
                # Expected params: [command]
                self._activate(payload["command"])

        except KeyError:
            print("Missing expected parameters: {}".format(directive))

    

    def _activate(self, command, speed=50):
        """
        Handles preset commands.
        :param command: the preset command
        :param speed: the speed if applicable
        """
        print("Activate command: ({}, {})".format(command, speed))
        
        if command in Command.RIGHT.value:
            self.shoulder.run_to_abs_pos(position_sp=-60, speed_sp=200, stop_action='hold')

        if command in Command.LEFT.value:
            self.shoulder.run_to_abs_pos(position_sp=60, speed_sp=200, stop_action='hold')
    
        if command in Command.STRAIGHT.value:
            self.shoulder.run_to_abs_pos(position_sp=0, speed_sp=200, stop_action='hold')
            
        if command in Command.GO.value: # shot
            t0 = time.perf_counter() 
            while time.perf_counter()-t0 < 5:
                self.elbow.run_forever(speed_sp=-1000)
                if time.perf_counter()-t0 > 0.45:
                    self.wrist.run_to_rel_pos(position_sp=80, speed_sp=300)
                    time.sleep(0.1)
                    self.elbow.stop()
                    break
            self.elbow.run_to_rel_pos(position_sp=180, speed_sp=100)
            self.elbow.run_to_abs_pos(position_sp=0, speed_sp=100)

        if command in Command.READY.value: # pick up a ball
            self.shoulder.run_to_abs_pos(position_sp=-255, speed_sp=200, stop_action='hold')
            time.sleep(4)
            self.wrist.run_to_rel_pos(position_sp=-80, speed_sp=400)
            
            

if __name__ == '__main__':

    # Startup sequence
    gadget = MindstormsGadget()
    gadget.sound.play_song((('C4', 'e'), ('D4', 'e'), ('E5', 'q')))
    gadget.leds.set_color("LEFT", "GREEN")
    gadget.leds.set_color("RIGHT", "GREEN")

    # Gadget main entry point
    gadget.main()

    # Shutdown sequence
    gadget.sound.play_song((('E5', 'e'), ('C4', 'e')))
    gadget.leds.set_color("LEFT", "BLACK")
    gadget.leds.set_color("RIGHT", "BLACK")
