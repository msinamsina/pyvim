from threading import Thread, Event
import msvcrt


class keyListener:
    def __init__(self):
        self.__stop_flag = True
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.__key = None
        self.__event = Event()
        self.start()

    def run(self):
        while self.__stop_flag:
            self.__key = msvcrt.getch().decode("utf-8")
            self.__event.set()
            self.__event.clear()

    def start(self):
        self.__stop_flag = True
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.__stop_flag = False

    def get_key(self):
        self.__event.wait()
        return self.__key

    def on_key(self, func):
        """A wrapper for keyListener.get_key() method."""
        def wrapper():
            while True:
                key = self.get_key()
                func(key)
        return wrapper

    def __del__(self):
        self.stop()


if __name__ == "__main__":
    key_listener = keyListener()

    @key_listener.on_key
    def print_key(key):
        print(key)
    print_key()
    while True:
        pass
