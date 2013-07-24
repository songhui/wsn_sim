"""
The config object contains the configuration variables for the WSN simulation.
This intended to be used as a mechanism to access some variables throughout
the simulation. Using the Config.xxx naming convention allows the reader to
immediately understand that this is a configuration variable. To facilitate
this, always use "import config", instead of "from config, import *"

Although, python does not prevent it, variables inside config are not meant
to be modified from anywhere

"""

COMPUTATIONAL_POWER = 100
BATTERY_POWER = 100
SIMULATION_TIME = 100000
COMPUTATIONAL_COST = 1
