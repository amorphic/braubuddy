import os
from xdg import BaseDirectory
import thermostat
import thermometer
import envcontroller
import output
import apps

def _get_user_config(config_dir):
    """
    Locate a braubuddy config file in the locations defined by the XDG spec.
    Otherwise return location of default config file.

    :param config_dir: Braubuddy application config dir.
    :type config_dir: :class`unicode`
    """

    for config_path in BaseDirectory.load_config_paths('braubuddy'):
        config_file_path = os.path.join(config_path, 'braubuddy')
        if os.path.isfile(config_file_path):
            return config_file_path
    print 'Loading braubuddy with default config.'
    print 'Please copy customised etc/braubuddy to one of these locations:'
    for path in BaseDirectory.xdg_config_dirs:
        print ' ' + os.path.join(path, 'braubuddy/')
    return os.path.join(CONFIG_DIR, 'braubuddy')

# Base dirs
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(THIS_DIR, 'config')
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')
# Internal config files
CONFIG_FILE_DASHBOARD = os.path.join(CONFIG_DIR, 'dashboard')
CONFIG_FILE_API = os.path.join(CONFIG_DIR, 'api')
# User config file
CONFIG_FILE_BRAUBUDDY = _get_user_config(os.path.join(CONFIG_DIR, 'braubuddy'))
# Recent state data
RECENT_DATA = output.ListMemoryOutput()
