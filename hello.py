import sys
import os
import ctypes as ct

# Glasswall Code
class Glasswall:
    """A Python API wrapper around the Glasswall library."""

    gwLibrary = None
    
    def __init__(self, pathToLib):
        """Constructor for the Glasswall library

        :param str pathToLib: The file path to the Glasswall library.
        """

        try:
            self.gwLibrary = ct.cdll.LoadLibrary(pathToLib)
        except Exception as e:
            raise Exception("Failed to load Glasswall library. Exception: {0}".format(e.message))
        
# Glasswall Code

class Log:
    @staticmethod
    def debug(content):
        line = "--[debug] " + content
        print(line)

def validate_github_volume(volume):
    os.curdir = volume
    items = os.listdir(volume)
    Log.debug("In Directory: " + volume)
    Log.debug(str(items))

def main():
    Log.debug("Starting Script")
    args = sys.argv[1:]
    Log.debug("Arguments: " + str(args))

    validate_github_volume(args[1])

    gw_lib_dir = "/home/glasswall/"
    os.curdir = gw_lib_dir
    items = os.listdir(gw_lib_dir)
    Log.debug("In Directory: " + os.curdir)
    Log.debug(str(items))
    gw = Glasswall(os.path.join( gw_lib_dir, "libglasswall.classic.so"))
    Log.debug("Loaded GW Rebuild Library")



    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(args[1]) for f in filenames if args[3] in f]

    Log.debug(str(result))

    Log.debug("Ending Script")



if __name__ == "__main__":
    main()