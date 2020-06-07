import sys
import os
from Glasswall import Glasswall

class Log:
    @staticmethod
    def debug(content):
        line = "--[debug] " + content
        print(line)

def main():
    Log.debug("Starting Script")
    args = sys.argv[1:]
    Log.debug("Arguments: " + str(args))

    volume = args[1]
    os.curdir = volume
    items = os.listdir(volume)
    Log.debug("In Directory: " + volume)
    Log.debug(str(items))

    gw_lib_dir = "/home/glasswall/"
    os.curdir = gw_lib_dir
    gw = Glasswall(gw_lib_dir)
    Log.debug("Loaded GW Rebuild Library")

    Log.debug("Ending Script")



if __name__ == "__main__":
    main()