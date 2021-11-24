""" DEVICE CONTROL FUNCTIONS: open, check_error, close """

import ctypes                     # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators

# load the dynamic library, get constants path (the path is OS specific)
if platform.startswith("win"):
    # on Windows
    dwf = ctypes.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = ctypes.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# import constants
path.append(constants_path)
import dwfconstants as constants

"""-----------------------------------------------------------------------"""

def open(device=None):
    """
        open a specific device

        parameters: - device type: None (first device), "Analog Discovery", "Analog Discovery 2", "Analog Discovery Studio", "Digital Discovery" and "Analog Discovery Pro 3X50"
    
        returns:    - the device handle
                    - the device name
    """
    device_names = [("Analog Discovery", constants.devidDiscovery), ("Analog Discovery 2", constants.devidDiscovery2),
                    ("Analog Discovery Studio", constants.devidDiscovery2), ("Digital Discovery", constants.devidDDiscovery),
                    ("Analog Discovery Pro 3X50", constants.devidADP3X50)]
    
    # decode device names
    device_type = constants.enumfilterAll
    for pair in device_names:
        if pair[0] == device:
            device_type = pair[1]
            break

    # count devices
    device_count = ctypes.c_int()
    dwf.FDwfEnum(device_type, ctypes.byref(device_count))

    # check for connected devices
    if device_count.value <= 0:
        if device_type.value == 0:
            print("Error: There are no connected devices")
        else:
            print("Error: There is no " + device + " connected")
        quit()

    # this is the device handle - it will be used by all functions to "address" the connected device
    device_handle = ctypes.c_int(0)

    # connect to the first available device
    index = 0
    while device_handle.value == 0 and index < device_count.value:
        dwf.FDwfDeviceOpen(ctypes.c_int(index), ctypes.byref(device_handle))
        index += 1  # increment the index and try again if the device is busy

    # check connected device type
    device_name = ""
    if device_handle.value != 0:
        device_id = ctypes.c_int()
        device_rev = ctypes.c_int()
        dwf.FDwfEnumDeviceType(ctypes.c_int(index - 1), ctypes.byref(device_id), ctypes.byref(device_rev))

        # decode device id
        for pair in device_names:
            if pair[1].value == device_id.value:
                device_name = pair[0]
                break

    return device_handle, device_name

"""-----------------------------------------------------------------------"""

def check_error(device_handle):
    """
        check for connection errors
    """
    # if the device handle is empty after a connection attempt
    if device_handle.value == constants.hdwfNone.value:
        # check for errors
        err_nr = ctypes.c_int()            # variable for error number
        dwf.FDwfGetLastError(ctypes.byref(err_nr))  # get error number
    
        # if there is an error
        if err_nr != constants.dwfercNoErc:
            # display it and quit
            err_msg = ctypes.create_string_buffer(512)        # variable for the error message
            dwf.FDwfGetLastErrorMsg(err_msg)                  # get the error message
            err_msg = err_msg.value.decode("ascii")           # format the message
            print("Error: " + err_msg)                        # display error message
            quit()                                            # exit the program
    return

"""-----------------------------------------------------------------------"""

def close(device_handle):
    """
        close a specific device
    """
    dwf.FDwfDeviceClose(device_handle)
    return
