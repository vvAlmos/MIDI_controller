def configure(description_file="./FPGA/MIDI_UI_Arty_S7.bit", device_name="ArtyS7", chip_index="0"):
    """
        configures the connected FPGA board

        parameters: - bit file
                    - device name
                    - chip index

        returns:    - True on success, False on error
    """
    # initialize the FPGA board
    process = Popen(["djtgcfg", "init", "-d", device_name],
                     stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("UTF-8")
    stderr = stderr.decode("UTF-8")

    # check response
    if stderr != "" or not ("Found Device ID" in stdout):
        return False

    # upload the bit file
    process = Popen(["djtgcfg", "prog", "-d", device_name,
                     "-i", chip_index, "-f", description_file],
                     stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("UTF-8")
    stderr = stderr.decode("UTF-8")

    # check response
    if stderr != "" or not ("Programming succeeded" in stdout):
        return False

    return True