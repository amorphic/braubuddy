import os
import shutil
from pkg_resources import Requirement, resource_filename
from xdg import BaseDirectory
import thermostat
import thermometer
import envcontroller
import output
import apps


def _deploy_config_file(destination_dir):
    """
    Copy the default Braubuddy config file to the given destnation directory.

    :param destination_dir: Config file destination dir.
    :type destination_dir: :class:`unicode`
    :returns: Path to deployed config file.
    :rtype: :class:`unicode`
    """

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    config_file_path = os.path.join(destination_dir, CONFIG_FILENAME_BRAUBUDDY)
    print 'Copying default config file to {0}'.format(config_file_path)
    default_config_path = os.path.join(CONFIG_DIR, CONFIG_FILENAME_BRAUBUDDY)
    shutil.copy(default_config_path, config_file_path)
    return config_file_path


def _get_config_file_location():
    """
    Locate a Braubuddy config file in the locations defined by the XDG spec.

    If no config file exists, deploy the default Braubuddy config file to the
    XDG config dir in the user's home dir ('~/.config/braubuddy/').

    :returns: Path to config file.
    :rtype: :class:`unicode`
    """

    for config_path in BaseDirectory.load_config_paths('braubuddy'):
        config_file_path = os.path.join(
            config_path, CONFIG_FILENAME_BRAUBUDDY)
        if os.path.isfile(config_file_path):
            break
    else:
        # No config file found. So deploy default config file to XDG config
        # dir in user home dir.
        config_path = os.path.join(
            BaseDirectory.xdg_config_home, 'braubuddy')
        config_file_path = _deploy_config_file(config_path)
    print 'Loading config from {0}'.format(config_file_path)
    return config_file_path

# Base dirs
THIS_DIR = resource_filename(Requirement.parse('braubuddy'), 'braubuddy')
CONFIG_DIR = os.path.join(THIS_DIR, 'config')
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')
# Internal config files
CONFIG_FILE_DASHBOARD = os.path.join(CONFIG_DIR, 'dashboard')
CONFIG_FILE_API = os.path.join(CONFIG_DIR, 'api')
# User config file
CONFIG_FILENAME_BRAUBUDDY = 'braubuddy'
CONFIG_FILE_BRAUBUDDY = _get_config_file_location()
# Recent state data
RECENT_DATA = output.ListMemoryOutput()
