import os
import thermostat
import thermometer
import envcontroller
import output
import apps

# Config files
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(THIS_DIR, 'config')
CONFIG_BRAUBUDDY = os.path.join(CONFIG_DIR, 'braubuddy')
CONFIG_DASHBOARD = os.path.join(CONFIG_DIR, 'dashboard')
CONFIG_API = os.path.join(CONFIG_DIR, 'api')
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')

# Recent state data
RECENT_DATA = output.ListMemory()
