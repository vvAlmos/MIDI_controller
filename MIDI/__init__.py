""" This module contains the functions needed to send MIDI messages """
""" More information: 
            https://github.com/ravelox/pimidi/tree/master/python """

"""-------------------------------------------------------------------"""
""" GLOBAL """
"""-------------------------------------------------------------------"""


import sys  # interactions with the interpreter
import socket   # socket operations
import struct   # conversion between Python values and C type data
from subprocess import Popen, PIPE # system calls
from message import *   # import all MIDI messages

sock = None

"""-------------------------------------------------------------------"""
""" INITIALIZATION """
"""-------------------------------------------------------------------"""


def open(configuration_file="./MIDI/address.conf", localport=5006):
    """
        start ravelomidi
        
        parameters: - configuration file path
                    - local port
    """
    # start raveloxmidi in the background
    Popen(["sudo", "raveloxmidi", "-c", configuration_file])

    global sock # load variable

    # local variables
    family = None
    connect_tuple = None

    # defining connection parameters
    # code snippet from the RaveloxMIDI examples
    if len(sys.argv) == 1:
        family = socket.AF_INET
        connect_tuple = ("localhost", localport)
    else:
        details = socket.getaddrinfo(
            sys.argv[1], localport, socket.AF_UNSPEC, socket.SOCK_DGRAM)
        family = details[0][0]
        if family == socket.AF_INET6:
            connect_tuple = (sys.argv[1], localport, 0, 0)
        else:
            connect_tuple = (sys.argv[1], localport)

    # connect socket
    sock = socket.socket(family, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect(connect_tuple)
    return


"""-------------------------------------------------------------------"""
""" SENDING """
"""-------------------------------------------------------------------"""


def send(msg_type, channel, data):
    """
        send a message
        
        parameters: - message type: from MIDI.message
                    - midi channel: 0-15
                    - data: from MIDI.message
    """
    # get data length
    length = len(data)

    # get message length
    byte_count = "B"
    for _ in range(length):
        byte_count = byte_count + "B"

    # construct the message
    # pack a binary structure with all the data words
    message = None
    if length == 1:
        message = struct.pack(byte_count, msg_type + channel, data[0])
    elif length == 2:
        message = struct.pack(byte_count, msg_type + channel, data[0], data[1])
    elif length == 3:
        message = struct.pack(byte_count, msg_type +
                              channel, data[0], data[1], data[2])
    elif length == 4:
        message = struct.pack(byte_count, msg_type + channel,
                              data[0], data[1], data[2], data[3])
    elif length == 5:
        message = struct.pack(byte_count, msg_type + channel,
                              data[0], data[1], data[2], data[3], data[4])
    elif length == 6:
        message = struct.pack(byte_count, msg_type + channel,
                              data[0], data[1], data[2], data[3], data[4], data[5])
    else:
        message = struct.pack(byte_count, msg_type + channel,
                              data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    # send message
    sock.send(message)
    return


"""-------------------------------------------------------------------"""
""" CLEANUP """
"""-------------------------------------------------------------------"""


def close():
    """
        stop ravelomidi
    """
    # close socket
    sock.close()

    # find remaining processes
    process = Popen(["sudo", "ps", "u"], stdout=PIPE, stderr=PIPE)
    stdout, _ = process.communicate()
    stdout = stdout.decode("UTF-8")
    processes = stdout.split("root")
    processes.pop(0)
    proc_id = []
    for index in range(len(processes)):
        processes[index] = processes[index].split()
        for property in processes[index]:
            if property == "raveloxmidi":
                proc_id.append(processes[index][0])
                continue

    # kill the processes
    success_flag = True
    for pid in proc_id:
        try:
            Popen(["sudo", "kill", "-SIGKILL", pid])
        except:
            success_flag = False
    return success_flag


"""-------------------------------------------------------------------"""
