import sys

class Log:
    @staticmethod
    def debug(content):
        line = "--[debug] " + content
        print(line)

def main():
    Log.debug("--[debug] Starting Script")
    args = sys.argv[1:]
    Log.debug(str(args))

    Log.debug("--[debug] Ending Script")



if __name__ == "__main__":
    main()