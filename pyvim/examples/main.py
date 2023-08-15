
if __name__ == "__main__":
    mode = 'insert'
    main_text = ""
    main_stdscr = curses.initscr()
    rows, cols = main_stdscr.getmaxyx()
    curses.noecho()
    banner = Banner(main_stdscr.subwin(rows - 10, cols, 10, 0), f"{rows} - {cols}")
    main_stdscr = curses.newwin(rows - 10, cols, 0, 0)
    main_stdscr.keypad(True)
    # main_stdscr.subwin()
    banner.start()
    data = '0'
    curs = 0
    cursx = 0
    while data != "q":
        data = main_stdscr.getkey()
        main_stdscr.clear()
        if mode == 'command':
            if data == "i":
                mode = 'insert'
            if data == "s":
                banner.stop()
            if data == "r":
                if not banner.thread.is_alive():
                    banner.start()
        else:
            if data == chr(curses.ascii.ESC):
                mode = 'command'
            elif data == "KEY_LEFT":
                if cursx % cols > 0:
                    curs -= 1
                    cursx -= 1
            elif data == "KEY_RIGHT":
                tmp = main_text.split('\n')[cursx // cols]
                main_stdscr.addstr(11, 0, f"{tmp}")
                if cursx % cols < len(tmp):
                    curs += 1
                    cursx += 1
            elif data == "KEY_UP":

                if cursx // cols > 0:
                    s = main_text.split('\n')
                    # curs -= curs % cols
                    if len(s[(cursx // cols) - 1]) > (cursx % cols):
                        cursx -= cols
                    else:
                        cursx -= ((cursx % cols) - len(s[(cursx // cols) - 1]))
                        cursx -= cols
                    s = '\n'.join(s[:(cursx // cols)])
                    curs = len(s) + (cursx % cols) + 1

            elif data == "KEY_DOWN":
                s = main_text.split('\n')
                if cursx // cols < len(s) - 1:
                    if len(s[(cursx // cols) + 1]) > (cursx % cols):
                        cursx += cols
                    else:
                        cursx -= ((cursx % cols) - len(s[(cursx // cols) + 1]))
                        cursx += cols - 1

                    s = '\n'.join(s[:(cursx // cols)])
                    curs = len(s) + (cursx % cols) + 1
                    # main_stdscr.addstr(12, 0, f"{s}")

            elif data == "KEY_DC":
                if curs < len(main_text):
                    # curs += 1
                    if main_text[curs + 1] == "\n":
                        cursx -= 1
                    main_text = main_text[:curs] + main_text[curs + 1:]
            elif ord(data) == 8:
                if curs > 0:
                    main_text = main_text[:curs - 1] + main_text[curs:]
                    curs -= 1
                    cursx -= 1
            elif data == '\n':
                main_text = main_text[:curs] + '\n' + main_text[curs:]
                curs += 1
                cursx += cols - (cursx % cols)
            else:
                curs += 1
                cursx += 1
                main_text = main_text[:curs] + data + main_text[curs:]
                main_stdscr.addstr(11, 0, f"{data}")
            main_stdscr.addstr(10, 0, f"{curs}, {cursx}, {cursx // cols}, {cursx % cols}")
        main_stdscr.addstr(0, 0, f"{main_text}")
        main_stdscr.move(cursx // cols, cursx % cols)
        main_stdscr.refresh()
    curses.endwin()
