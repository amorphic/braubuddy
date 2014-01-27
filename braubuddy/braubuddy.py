"""
Braubuddy core
"""

import thermometer
import thermostat
import envcontroller
import cherrypy
import sys

class BraubuddyWeb(object):
    """
    The web interface.
    """

    def __init__():
        # load from config

    def index(self):
        return 'Blaaaaaah'
    index.exposed = True

class BraubuddyEngine(object):
    """
    The engine.
    """

    def __init__():
        # load from config

def main():

    # start a thread running the engine
    # start a thread running the web
    cherrypy.quickstart(BraubuddyWeb()) 

if __name__ == '__main__':
    sys.exit(main())
