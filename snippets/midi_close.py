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
