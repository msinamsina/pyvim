from threading import Thread
import curses
import time


class MovingText:
    def __init__(self, stdscr, text):
        self.__stdscr = stdscr
        self.__rows, self.__cols = self.__stdscr.getmaxyx()
        self.__text = text
        self.__cnt = 0
        self.__stdscr.keypad(True)
        self.__stdscr.clear()
        self.__stdscr.refresh()
        self.__stop_flag = True
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.__cnt = 0
        super().__init__()

    def __get_height_width(self) -> tuple:
        rows, cols = self.__stdscr.getmaxyx()
        self.__rows = rows
        self.__cols = cols
        return rows, cols

    def run(self) -> None:
        win = None
        x, y = curses.getsyx()
        while self.__stop_flag:
            rows, cols = self.__get_height_width()
            win = self.__stdscr.subwin(2, cols, rows - 2, 0)
            rows, cols = win.getmaxyx()

            win.clear()
            if self.__cnt + len(self.__text) >= cols:
                text1 = self.__text[:cols - self.__cnt - 1]
                text2 = self.__text[cols - self.__cnt - 1:]
                win.addstr(1, cols - len(text1) - 1, text1)
                win.addstr(1, 0, text2)
            else:
                win.addstr(1, self.__cnt, self.__text)
            win.refresh()
            self.__cnt += 1
            self.__cnt = self.__cnt % (cols - 1)
            time.sleep(1)
            self.__stdscr.move(x, y)
            self.__stdscr.refresh()

    def start(self) -> None:
        self.__stop_flag = True
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.__stop_flag = False
