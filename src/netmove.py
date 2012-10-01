""" Simple ``move'' animation. Use w,a,s,d to move, q to stop"""
#import led
import sync
import curses
__import__('sys').path.append('./net')
import ledremote

#s = led.LedScreen()
s = ledremote.RemoteLedScreen('nodejs', 8000)
print s

window = curses.initscr()
curses.raw()
curses.noecho()
window.nodelay(True)

pos = (0, 0)

lastch = -1

metronome = sync.Metronome(fps=25.)
metronome.start()

try:
    while True:
        for x in range(12):
            for y in range(10):
                s[(x, y)] = 25, 25, 25

        # Set our pos
        s[(pos[0], pos[1])] = 255, 0, 0

        # get ch, if -1, then no char is available
        f = window.getch()
        # quit if f == q
        if f == ord('q'):
            break

        if f != -1:
            lastch = f

        if lastch == ord('w'):
            if pos[0]+1>11:
                pos = (0, pos[1])
            else:
                pos = (pos[0]+1,pos[1])
        elif lastch == ord('s'):
            if pos[0] - 1 < 0:
                pos = (11, pos[1])
            else:
                pos = (pos[0]-1, pos[1])
        elif lastch == ord('a'):
            if pos[1]+1 > 9:
                pos = (pos[0], 0)
            else:
                pos = (pos[0], pos[1]+1)
        elif lastch == ord('d'):
            if pos[1]-1 < 0:
                pos = (pos[0], 9)
            else:
                pos = (pos[0],pos[1]-1)

        s.push()

        metronome.sync()

finally:
    curses.reset_shell_mode()

