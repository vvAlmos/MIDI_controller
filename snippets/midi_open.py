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
