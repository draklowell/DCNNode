import threading
import ctypes


class Console:
    def __init__(self):
        pass

    def print(self, text, end="\n"):
        print(text, end=end)
        
    def close(self):
        pass
