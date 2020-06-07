import ctypes as ct

class GwStringReturnObj:
    """A result from Glasswall containing a text string."""
    def __init__(self):
        pass

    text = None  # type: str or None


class GwFileTypeEnum:
    """A result from Glasswall containing the determined file type value."""
    def __init__(self):
        pass

    enumValue = 0  # type: int
    fileBuffer = None # type: bytearray or None

class GwStatusReturnObj:
    """A result from Glasswall containing the return status."""

    def __init__(self):
        pass

    returnStatus = 0  # type: int


class GwProcessStatusReturnObj:
    """A result from Glasswall containing the return status along with the process status."""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    processStatus = 0  # type:int


class GwConfigReturnObj:
    """A result from Glasswall containing the return status along with the text string"""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    string = None  # type: str or None


class GwMemReturnObj:
    """A result from Glasswall containing the return status along with the file buffer"""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    fileBuffer = None  # type: bytearray or None


class GwFileToMemPlusReportReturnObj:
    """A result from Glasswall containing the return status along with the file buffer and the engineering report"""

    def __init__(self):
        pass

    returnStatus = 0  # type: int
    fileBuffer = None  # type: bytearray or None
    reportBuffer = None  # type: bytearray or None

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
        
    def GWFileConfigXML(self, xmlString):
        """Applies the given XML content management configuration to the Glasswall library.

        :param str xmlString: The XML content management configuration.
        :return: A result indicating the status of the call.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileConfigXML.argtypes = [ct.c_wchar_p]

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileConfigXML(
            ct.c_wchar_p(xmlString)
        )

        return gwReturn

    def GWFileConfigGet(self):
        """Retrieves the current XML content management configuration from the Glasswall library.

        :return: A result indicating the status of the call along with the XML content management configuration.
        :rtype: GwConfigReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileConfigGet.argtypes = [
            ct.POINTER(ct.POINTER(ct.c_wchar)),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_configurationBuffer = ct.POINTER(ct.c_wchar)()
        ct_size = ct.c_size_t(0)

        # Return Object
        gwReturn = GwConfigReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileConfigGet(
            ct.byref(ct_configurationBuffer),
            ct.byref(ct_size)
        )

        # Convert outputBuffer to python string
        gwReturn.string = ct.wstring_at(ct_configurationBuffer)

        return gwReturn

    def GWFileConfigRevertToDefaults(self):
        """Reverts the content management settings to their defaults, which are described in the Glasswall SDK documentation.

        :return: A result indicating the status of the call
        :rtype: GwStatusReturnObj
        """

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileConfigRevertToDefaults()

        return gwReturn

    def GWGetIdInfo(self, issueId):
        """Retrieves the group description for the given Issue ID.

        :param int issueId: The Issue ID to lookup.
        :return: A result indicating the status of the call along with the Issue ID group description.
        :rtype: GwConfigReturnObj
        """

        # API function declaration
        self.gwLibrary.GWGetIdInfo.argtypes = [
            ct.c_uint32,
            ct.POINTER(ct.c_size_t),
            ct.POINTER(ct.POINTER(ct.c_char)),
        ]

        # Variable initialisation
        ct_issueId = ct.c_uint32(issueId)
        ct_size = ct.c_size_t(0)
        ct_descString = ct.POINTER(ct.c_char)()

        # Return Object
        gwReturn = GwConfigReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWGetIdInfo(
            ct_issueId,
            ct.byref(ct_size),
            ct.byref(ct_descString)
        )

        # Convert outputBuffer to python string
        strBuffer = ct.string_at(ct_descString, ct_size.value)
        gwReturn.string = strBuffer.decode("utf-8")

        return gwReturn

    def GWGetAllIdInfo(self):
        """Retrieves the XML containing all the Issue ID ranges with their group descriptions.

        :return: A result indicating the status of the call along with all of the Issue ID information.
        :rtype: GwConfigReturnObj
        """

        # API function declaration
        self.gwLibrary.GWGetAllIdInfo.argtypes = [
            ct.POINTER(ct.c_size_t),
            ct.POINTER(ct.POINTER(ct.c_char))
        ]

        # Variable initialisation
        ct_size = ct.c_size_t(0)
        ct_xmlString = ct.POINTER(ct.c_char)()

        # Return Object
        gwReturn = GwConfigReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWGetAllIdInfo(
            ct.byref(ct_size),
            ct.byref(ct_xmlString)
        )

        # Convert outputBuffer to python string
        strBuffer = ct.string_at(ct_xmlString, ct_size.value)
        gwReturn.string = strBuffer.decode("utf-8")

        return gwReturn

    def GWFileProtectLite(self, inputFilePath, fileType):
        """Protects the file in File to Memory Protect Lite mode. The file buffer will be None if the file is non-conforming.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :return: A result indicating the file process status along with the protected file.
        """

        # API function declaration
        self.gwLibrary.GWFileProtectLite.argtypes = [
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
        gwReturn.returnStatus = self.gwLibrary.GWFileProtectLite(
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

    def GWFileAnalysisAudit(self, inputFilePath, fileType):
        """Analyses the file in File to Memory Analysis mode.

        :param str inputFilePath: The file path to the file to be analysed.
        :param str fileType: The file type of the file to be analysed.
        :return: A result indicating the file process status along with the XML analysis report.
        :rtype: GwMemReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileAnalysisAudit.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_analysisFileBuffer = ct.c_void_p(0)
        ct_size = ct.c_size_t(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileAnalysisAudit(
            ct_filePath,
            ct_fileType,
            ct.byref(ct_analysisFileBuffer),
            ct.byref(ct_size)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_size.value)()
        ct.memmove(fileBuffer, ct_analysisFileBuffer.value, ct_size.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWFileToFileProtectLite(self, inputFilePath, fileType, outputFilePath):
        """Protects the file in File to File Protect Lite mode. The managed file will not be created if the output directory does not exist or if the file is non-conforming.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :param str outputFilePath: The output file path to the managed file.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileProtectLite.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_outputFilePath = ct.c_wchar_p(outputFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileProtectLite(
            ct_inputFilePath,
            ct_fileType,
            ct_outputFilePath
        )

        return gwReturn

    def GWFileToFileProtect(self, inputFilePath, fileType, outputFilePath):
        """Protects the file in File to File Protect mode. The managed file will not be created if the output directory does not exist or if the file is non-conforming.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :param str outputFilePath: The output file path to the managed file.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileProtect.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_outputFilePath = ct.c_wchar_p(outputFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileProtect(
            ct_inputFilePath,
            ct_fileType,
            ct_outputFilePath
        )

        return gwReturn

    def GWFileToFileAnalysisAudit(self, inputFilePath, fileType, analysisFilePath):
        """Analyses the file in File to File Analysis mode. The XML analysis report will not be created if the output directory does not exist.

        :param str inputFilePath: The file path to the file to be analysed.
        :param str fileType: The file type of the file to be analysed.
        :param str analysisFilePath: The output file path to the XML analysis report.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileAnalysisAudit.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_analysisFilePath = ct.c_wchar_p(analysisFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileAnalysisAudit(
            ct_inputFilePath,
            ct_fileType,
            ct_analysisFilePath
        )

        return gwReturn

    def GWFileToFileAnalysisProtectAndExport(self, inputFilePath, exportFilePath):
        """Exports the file in File to File Export mode. The exported archive will not be created if the output directory does not exist.

        :param str inputFilePath: The file path to the file to be processed.
        :param str exportFilePath: The output file path to the exported archive.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileAnalysisProtectAndExport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_exportFilePath = ct.c_wchar_p(exportFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileAnalysisProtectAndExport(
            ct_inputFilePath,
            ct_exportFilePath
        )

        return gwReturn

    def GWFileToFileProtectAndImport(self, inputFilePath, outputFilePath):
        """Imports the exported archive in File to File Import mode. The imported file will not be created if the output directory does not exist or the file is non-conforming.

        :param str inputFilePath: The file path to the exported file archive.
        :param str outputFilePath: The output file path to the imported file.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        self.gwLibrary.GWFileToFileProtectAndImport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_outputFilePath = ct.c_wchar_p(outputFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileProtectAndImport(
            ct_inputFilePath,
            ct_outputFilePath
        )

        return gwReturn

    def GWFileToMemoryProtectAndImport(self, inputFilePath):
        """Imports the exported archive in File to Memory Import mode.

        :param str inputFilePath: The file path to the exported file archive.
        :return: A result indicating the file process status along with the imported file.
        :rtype: GwMemReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToMemoryProtectAndImport.argtypes = [
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_outputFileBuffer = ct.c_void_p(0)
        ct_size = ct.c_size_t(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToMemoryProtectAndImport(
            ct_filePath,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_size)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_size.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_size.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWFileToMemoryAnalysisProtectAndExport(self, inputFilePath):
        """Exports the file in File to Memory Export mode.

        :param str inputFilePath: The file path to the file to be processed.
        :return: A result indicating the file process status along with the exported file archive.
        :rtype: GwMemReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToMemoryAnalysisProtectAndExport.argtypes = [
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_size = ct.c_size_t(0)
        ct_outputFileBuffer = ct.c_void_p(0)

        # Return Object
        gwReturn = GwMemReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToMemoryAnalysisProtectAndExport(
            ct_filePath,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_size)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_size.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_size.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWFileProtectLiteAndReport(self, inputFilePath, fileType):
        """Protects the file in File to Memory Protect Lite with engineering report mode.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :return: A result indicating the file process status along with the protected file and the engineering report.
        :rtype: GwFileToMemPlusReportReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileProtectLiteAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t),
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)

        ct_outputFileBuffer = ct.c_void_p(0)
        ct_fileBufferSize = ct.c_size_t(0)

        ct_outputReportBuffer = ct.c_void_p(0)
        ct_reportBufferSize = ct.c_size_t(0)

        # Return Object
        gwReturn = GwFileToMemPlusReportReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileProtectLiteAndReport(
            ct_filePath,
            ct_fileType,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_fileBufferSize),
            ct.byref(ct_outputReportBuffer),
            ct.byref(ct_reportBufferSize)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_fileBufferSize.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_fileBufferSize.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        reportBuffer = (ct.c_byte * ct_reportBufferSize.value)()
        ct.memmove(reportBuffer, ct_outputReportBuffer.value, ct_reportBufferSize.value)
        gwReturn.reportBuffer = bytearray(reportBuffer)

        return gwReturn

    def GWFileProtectAndReport(self, inputFilePath, fileType):
        """Protects the file in File to Memory Protect with engineering report mode.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :return: A result indicating the file process status along with the protected file and the engineering report.
        :rtype: GwFileToMemPlusReportReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileProtectAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t),
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)

        ct_outputFileBuffer = ct.c_void_p(0)
        ct_fileBufferSize = ct.c_size_t(0)

        ct_outputReportBuffer = ct.c_void_p(0)
        ct_reportBufferSize = ct.c_size_t(0)

        # Return Object
        gwReturn = GwFileToMemPlusReportReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileProtectAndReport(
            ct_filePath,
            ct_fileType,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_fileBufferSize),
            ct.byref(ct_outputReportBuffer),
            ct.byref(ct_reportBufferSize)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_fileBufferSize.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_fileBufferSize.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        reportBuffer = (ct.c_byte * ct_reportBufferSize.value)()
        ct.memmove(reportBuffer, ct_outputReportBuffer.value, ct_reportBufferSize.value)
        gwReturn.reportBuffer = bytearray(reportBuffer)

        return gwReturn

    def GWFileToFileProtectLiteAndReport(self, inputFilePath, fileType, outputFilePath, reportFilePath):
        """Protects the file in File to File Protect Lite with engineering report mode. The managed file will not be created if the output directory does not exist or the file is non-conforming. The engineering report will not be created if the output directory does not exist.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :param str outputFilePath: The output file path to the managed file.
        :param str reportFilePath: The output file path to the engineering report.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileProtectLiteAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)

        ct_outputFilePath = ct.c_wchar_p(outputFilePath)
        ct_reportFilePath = ct.c_wchar_p(reportFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileProtectLiteAndReport(
            ct_inputFilePath,
            ct_fileType,
            ct_outputFilePath,
            ct_reportFilePath
        )

        return gwReturn

    def GWFileToFileProtectAndReport(self, inputFilePath, fileType, outputFilePath, reportFilePath):
        """Protects the file in File to File Protect with engineering report mode. The managed file will not be created if the output directory does not exist or the file is non-conforming. The engineering report will not be created if the output directory does not exist.

        :param str inputFilePath: The file path to the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :param str outputFilePath: The output file path to the managed file.
        :param str reportFilePath: The output file path to the engineering report.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileProtectAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_outputFilePath = ct.c_wchar_p(outputFilePath)
        ct_reportFilePath = ct.c_wchar_p(reportFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileProtectAndReport(
            ct_inputFilePath,
            ct_fileType,
            ct_outputFilePath,
            ct_reportFilePath
        )

        return gwReturn

    def GWFileAnalysisAuditAndReport(self, inputFilePath, fileType):
        """Analyses the file in File to Memory Analysis with engineering report mode.

        :param str inputFilePath: The file path to the file to be analysed.
        :param str fileType: The file type of the file to be analysed.
        :return: A result indicating the file process status along with the XML analysis report and the engineering report.
        :rtype: GwFileToMemPlusReportReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileAnalysisAuditAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t),
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)

        ct_outputFileBuffer = ct.c_void_p(0)
        ct_fileBufferSize = ct.c_size_t(0)

        ct_outputReportBuffer = ct.c_void_p(0)
        ct_reportBufferSize = ct.c_size_t(0)

        # Return Object
        gwReturn = GwFileToMemPlusReportReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileAnalysisAuditAndReport(
            ct_filePath,
            ct_fileType,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_fileBufferSize),
            ct.byref(ct_outputReportBuffer),
            ct.byref(ct_reportBufferSize)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_fileBufferSize.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_fileBufferSize.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        reportBuffer = (ct.c_byte * ct_reportBufferSize.value)()
        ct.memmove(reportBuffer, ct_outputReportBuffer.value, ct_reportBufferSize.value)
        gwReturn.reportBuffer = bytearray(reportBuffer)

        return gwReturn

    def GWFileToFileAnalysisAuditAndReport(self, inputFilePath, fileType, outputFilePath, reportFilePath):
        """Analyses the file in File to File Analysis with engineering report mode. The XML analysis report will not be created if the output directory does not exist. The engineering report will not be created if the output directory does not exist.

        :param str inputFilePath: The file path to the file to be analysed.
        :param str fileType: The file type of the file to be analysed.
        :param str outputFilePath: The output file path to the XML analysis report.
        :param str reportFilePath: The output file path to the engineering report.
        :return: A result indicating the file process status.
        :rtype: GwStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileToFileAnalysisAuditAndReport.argtypes = [
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p,
            ct.c_wchar_p
        ]

        # Variable initialisation
        ct_inputFilePath = ct.c_wchar_p(inputFilePath)
        ct_fileType = ct.c_wchar_p(fileType)
        ct_outputFilePath = ct.c_wchar_p(outputFilePath)
        ct_reportFilePath = ct.c_wchar_p(reportFilePath)

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileToFileAnalysisAuditAndReport(
            ct_inputFilePath,
            ct_fileType,
            ct_outputFilePath,
            ct_reportFilePath
        )

        return gwReturn

    def GWMemoryToMemoryProtect(self, inputFileBuffer, fileType):
        """Protects the file in Memory to Memory Protect mode. The file buffer will be None if the file is non-conforming.

        :param bytearray inputFileBuffer: The buffer containing the file to be processed.
        :param str fileType: The file type of the file to be processed.
        :return: A result indicating the file process status along with the protected file.
        :rtype: GwMemReturnObj
        """

        self.gwLibrary.GWMemoryToMemoryProtect.argtypes = [
            ct.c_void_p,
            ct.c_size_t,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialization
        byteArrayBuffer     = bytearray(inputFileBuffer)
        ct_buffer           = (ct.c_ubyte * len(byteArrayBuffer)).from_buffer(byteArrayBuffer)
        ct_length           = ct.c_size_t(len(inputFileBuffer))
        ct_fileType         = ct.c_wchar_p(fileType)
        ct_outputFileBuffer = ct.c_void_p(0)
        ct_fileBufferSize   = ct.c_size_t(0)

        gwReturn = GwMemReturnObj()

        gwReturn.returnStatus = self.gwLibrary.GWMemoryToMemoryProtect(
            ct.byref(ct_buffer),
            ct_length,
            ct_fileType,
            ct.byref(ct_outputFileBuffer),
            ct.byref(ct_fileBufferSize)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_fileBufferSize.value)()
        ct.memmove(fileBuffer, ct_outputFileBuffer.value, ct_fileBufferSize.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWMemoryToMemoryAnalysisAudit(self, inputFileBuffer, fileType):
        """Analyses the file in Memory to Memory analysis mode.

        :param bytearray inputFileBuffer: The buffer containing the file to be analysed.
        :param str fileType: The file type of the file to be analysed.
        :return: A result indicating the file process status along with the XML analysis report.
        :rtype: GwMemReturnObj
        """

        self.gwLibrary.GWMemoryToMemoryAnalysisAudit.argtypes = [
            ct.c_void_p,
            ct.c_size_t,
            ct.c_wchar_p,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialization
        byteArrayBuffer         = bytearray(inputFileBuffer)
        ct_buffer               = (ct.c_ubyte * len(byteArrayBuffer)).from_buffer(byteArrayBuffer)
        ct_length               = ct.c_size_t(len(inputFileBuffer))
        ct_fileType             = ct.c_wchar_p(fileType)
        ct_analysisOutputBuffer = ct.c_void_p(0)
        ct_analysisBufferSize   = ct.c_size_t(0)

        gwReturn = GwMemReturnObj()

        gwReturn.returnStatus = self.gwLibrary.GWMemoryToMemoryAnalysisAudit(
            ct.byref(ct_buffer),
            ct_length,
            ct_fileType,
            ct.byref(ct_analysisOutputBuffer),
            ct.byref(ct_analysisBufferSize)
        )

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_analysisBufferSize.value)()
        ct.memmove(fileBuffer, ct_analysisOutputBuffer.value, ct_analysisBufferSize.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWFileProcessStatus(self):
        """Retrieves the process status from the previous call made to Glasswall.

        :return: A result indicating the status of the call along with the process status.
        :rtype: GwProcessStatusReturnObj
        """

        # API function declaration
        self.gwLibrary.GWFileProcessStatus.argtypes = [ct.POINTER(ct.c_uint)]

        # Variable initialisation
        ct_glasswallProcessStatus = ct.c_uint(0)

        # Return Object
        gwReturn = GwProcessStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileProcessStatus(ct.byref(ct_glasswallProcessStatus))
        gwReturn.processStatus = ct_glasswallProcessStatus.value

        return gwReturn

    def GWDetermineFileTypeFromFile(self, filePath):
        """Returns a value indicating the file type determined by Glasswall.

        :param str filePath: The file path to the input file.
        :return: A result indicating the determined file type.
        :rtype: GwFileTypeEnum
        """

        # API function declaration
        self.gwLibrary.GWDetermineFileTypeFromFile.argtypes = [ct.c_wchar_p]

        # Variable initialisation
        ct_filePath = ct.c_wchar_p(filePath)

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API Call
        gwReturn.enumValue = self.gwLibrary.GWDetermineFileTypeFromFile(ct_filePath)

        return gwReturn

    def GWDetermineFileTypeFromFileAndReport(self, filePath):
        """Returns a value indicating the file type determined by Glasswall along with an XML Analysis Report.

        :param str filePath: The file path to the input file.
        :return: A result indicating the determined file type along with an XML analysis report.
        :rtype: GwFileTypeEnum
        """

        # API function declaration
        self.gwLibrary.GWDetermineFileTypeFromFileAndReport.argtypes = [
            ct.c_wchar_p, 
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation
        ct_filePath                 = ct.c_wchar_p(filePath)
        ct_analysisFileBuffer       = ct.c_void_p(0)
        ct_analysisFileBufferLength = ct.c_size_t(0)

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API Call
        gwReturn.enumValue = self.gwLibrary.GWDetermineFileTypeFromFileAndReport(ct_filePath, ct.byref(ct_analysisFileBuffer), ct.byref(ct_analysisFileBufferLength))

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_analysisFileBufferLength.value)()
        ct.memmove(fileBuffer, ct_analysisFileBuffer.value, ct_analysisFileBufferLength.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWDetermineFileTypeFromFileInMem(self, inputFileBuffer):
        """Returns a value indicating the file type determined by Glasswall.

        :param bytearray inputFileBuffer: The input buffer containing the file to be determined.
        :return: A result indicating the determined file type.
        :rtype: GwFileTypeEnum
        """

        # API function declaration
        self.gwLibrary.GWDetermineFileTypeFromFileInMem.argtypes = [
            ct.c_void_p,
            ct.c_size_t
        ]

        # Variable initialisation

        byteArrayBuffer             = bytearray(inputFileBuffer)
        ct_inputFileBuffer          = (ct.c_ubyte * len(byteArrayBuffer)).from_buffer(byteArrayBuffer)
        ct_inputFileBufferLength    = ct.c_size_t(len(byteArrayBuffer))

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API Call
        gwReturn.enumValue = self.gwLibrary.GWDetermineFileTypeFromFileInMem(ct.byref(ct_inputFileBuffer), ct_inputFileBufferLength)

        return gwReturn

    def GWDetermineFileTypeFromFileInMemAndReport(self, inputFileBuffer):
        """Returns a value indicating the file type determined by Glasswall along with an XML analysis report.

        :param bytearray inputFileBuffer: The input buffer containing the file to be determined.
        :return: A result indicating the determined file type along with an XML analysis report.
        :rtype: GwFileTypeEnum
        """

        # API function declaration
        self.gwLibrary.GWDetermineFileTypeFromFileInMemAndReport.argtypes = [
            ct.c_void_p,
            ct.c_size_t,
            ct.POINTER(ct.c_void_p),
            ct.POINTER(ct.c_size_t)
        ]

        # Variable initialisation

        byteArrayBuffer             = bytearray(inputFileBuffer)
        ct_inputFileBuffer          = (ct.c_ubyte * len(byteArrayBuffer)).from_buffer(byteArrayBuffer)
        ct_inputFileBufferLength    = ct.c_size_t(len(byteArrayBuffer))
        ct_analysisFileBuffer       = ct.c_void_p(0)
        ct_analysisFileBufferLength = ct.c_size_t(0)

        # Return Object
        gwReturn = GwFileTypeEnum()

        # API Call
        gwReturn.enumValue = self.gwLibrary.GWDetermineFileTypeFromFileInMemAndReport(ct.byref(ct_inputFileBuffer), ct_inputFileBufferLength, ct.byref(ct_analysisFileBuffer), ct.byref(ct_analysisFileBufferLength))

        # Convert outputBuffer to python bytearray
        fileBuffer = (ct.c_byte * ct_analysisFileBufferLength.value)()
        ct.memmove(fileBuffer, ct_analysisFileBuffer.value, ct_analysisFileBufferLength.value)
        gwReturn.fileBuffer = bytearray(fileBuffer)

        return gwReturn

    def GWFileDone(self):
        """Releases any resources allocated by the Glasswall library. This is normally called once all the processing is done and Glasswall is not required anymore.

        :return: A result indicating the status of the call.
        :rtype: GwStatusReturnObj
        """

        # Return Object
        gwReturn = GwStatusReturnObj()

        # API Call
        gwReturn.returnStatus = self.gwLibrary.GWFileDone()

        return gwReturn

    def GWFileVersion(self):
        """Returns the Glasswall library version.

        :return: A result with the Glasswall library version.
        :rtype: GwStringReturnObj
        """

        # Declare the return type
        self.gwLibrary.GWFileVersion.restype = ct.POINTER(ct.c_wchar)

        # Return Object
        gwReturn = GwStringReturnObj()

        # API Call
        ct_string = self.gwLibrary.GWFileVersion()

        gwReturn.text = ct.wstring_at(ct_string)

        return gwReturn

    def GWFileProcessMsg(self):
        """Returns the file process message from the previous call made to Glasswall.

        :return: A result with the file process message.
        :rtype: GwStringReturnObj
        """

        # Declare the return type
        self.gwLibrary.GWFileProcessMsg.restype = ct.POINTER(ct.c_wchar)

        # Return Object
        gwReturn = GwStringReturnObj()

        # API Call
        ct_string = self.gwLibrary.GWFileProcessMsg()

        gwReturn.text = ct.wstring_at(ct_string)

        return gwReturn

    def GWFileErrorMsg(self):
        """Returns the file error message from the previous call made to Glasswall.

        :return: A result with the file error message.
        :rtype: GwStringReturnObj
        """

        # Declare the return type
        self.gwLibrary.GWFileErrorMsg.restype = ct.POINTER(ct.c_wchar)

        # Return Object
        gwReturn = GwStringReturnObj()

        # API Call
        ct_string = self.gwLibrary.GWFileErrorMsg()

        gwReturn.text = ct.wstring_at(ct_string)

        return gwReturn