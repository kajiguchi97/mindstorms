# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# 
# You may not use this file except in compliance with the terms and conditions 
# set forth in the accompanying LICENSE.TXT file.
#
# THESE MATERIALS ARE PROVIDED ON AN "AS IS" BASIS. AMAZON SPECIFICALLY DISCLAIMS, WITH 
# RESPECT TO THESE MATERIALS, ALL WARRANTIES, EXPRESS, IMPLIED, OR STATUTORY, INCLUDING 
# THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.


"""
The Alexa Gadgets Python API allows you to build fun and delightful accessories
that pair to compatible Echo devices via Bluetooth. These accessories can
extend Alexa’s capabilities to new modalities with motors, lights, sound chips,
and more.

.. highlight:: python
.. code-block:: python

    from agt import AlexaGadget

    class MyFirstGadget(AlexaGadget):
        def on_alexa_gadget_statelistener_stateupdate(self, directive):
            print("STATE UPDATED: ", directive)

    if __name__ == '__main__':
        MyFirstGadget().main()

"""
# Core API
from agt.alexa_gadget import AlexaGadget

# Directives
from agt.messages_pb2 import Directive
from agt.messages_pb2 import ClearIndicatorDirective
from agt.messages_pb2 import DeleteAlertDirective
from agt.messages_pb2 import DiscoverDirective
from agt.messages_pb2 import SetAlertDirective
from agt.messages_pb2 import SetIndicatorDirective
from agt.messages_pb2 import SpeechmarksDirective
from agt.messages_pb2 import StateUpdateDirective
from agt.messages_pb2 import TempoDirective

# Events
from agt.messages_pb2 import Event
from agt.messages_pb2 import DiscoverResponseEvent

