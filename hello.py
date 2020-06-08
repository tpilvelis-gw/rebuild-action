import sys
import os
import ctypes as ct

# Glasswall Code
class GwMemReturnObj:
    """A result from Glasswall containing the return status along with the file buffer"""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    fileBuffer = None  # type: bytearray or None

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
        

    def GWFileProtect(self, inputFilePath, fileType):
        """Protects the file in File to Memory Protect mode. The file buffer will be None if the file is non-conforming.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :return: A result indicating the file process status along with the protected file.
        :rtype: GwMemReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileProtect.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_fileBuffer = ct.c_void_p(0)
        ct_size = ct.c_size_t(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileProtect(
            ct_filePath,
            ct_fileType,
            ct.byref(ct_fileBuffer),
            ct.byref(ct_size)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_size.value)()
        ct.memmove(fileBuffer, ct_fileBuffer.value, ct_size.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

# Glasswall Code

class Log:
    @staticmethod
    def debug(content):
        line = "--[debug] " + content
        print(line)

    @staticmethod
    def report(content):
        line = "--[info] " + content
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

    #Get files with ARG filetype
    files_to_rebuild = [os.path.join(dp, f) for dp, dn, filenames in os.walk(args[1]) for f in filenames if args[3] in f]
    
    Log.report("Files to Rebuild")
    Log.report(str(files_to_rebuild))

    report1_h = "File"
    report2_h = "Status Code"
    Log.report(report1_h.ljust(20)+"|"+ report2_h.rjust(12))
    for f in files_to_rebuild:
        protected_f = gw.GWFileProtect(f, args[3])
        Log.report(f.ljust(20)+"|"+ str(protected_f.returnStatus).rjust(12))

    Log.debug("Ending Script")



if __name__ == "__main__":
    main()