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
