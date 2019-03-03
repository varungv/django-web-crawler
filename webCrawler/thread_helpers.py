import threading


def print_running_threads():
    print("Running Threads are :" + str(threading.enumerate()))


def number_of_threads_running():
    return "Threads running: " + str(len(threading.enumerate()))