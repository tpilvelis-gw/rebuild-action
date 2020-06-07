import sys
import os

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


    Log.debug("Ending Script")



if __name__ == "__main__":
    main()