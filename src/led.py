"""Low-level interface to the LED Wall at TechInc. http://techinc.nl"""

import sys
sys.path.append('../lib/uspp')

# Python serial communication module. Get it from pypi.
try:
    import uspp
except:
    print 'Error: USPP module missing!'
    # Do not stop, documentation parser doesn't require uspp.

from transform import transform_led, reverse_led

__all__ = ['LedScreenException', 'LedScreen']

class LedScreenException(Exception):
    pass

class LedScreen(object):
    """
    The low-level LED wall screen.
    """

    def __init__(self, fname='/dev/ttyACM0', brate=115200, dim=(12,10), gamma=2.2):
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.tty = uspp.SerialPort(fname, speed=brate, timeout=0)
        self.w, self.h = dim
        self.buf = [(0, 0, 0)] * self.w * self.h

        set_transform(*dim)

        gamma = float(gamma)
        max_gamma = 255.**gamma
        self.gamma_map = [ int( (1 + 2 * x**gamma / (max_gamma/255.)) //2 ) for x in xrange(256) ]

    def gamma_correct(self, colour):
        return tuple(self.gamma_map[c] for c in colour)

    def __setitem__(self, tup, val):
        """
        Allows for easy frame access.
        """
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        if tup[0] not in range(0, self.w) or tup[1] not in range(0, self.h):
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        self.buf[reverse_led(tup)] = self.gamma_correct(val)

        waiting = self.tty.inWaiting()
        if waiting > 0:
            _ = self.tty.read(waiting)

    def push(self):
        """
        Push the current frame contents to the screen
        """
        for ind, val in enumerate(self.buf):
            self.tty.write(chr(ind) + ''.join(map(lambda x: chr(x), val)))

    def load_frame(self, frame):
        """
        Load internal frame from *frame*. Does not send anything yet.
        """
        for y in xrange(max(len(frame), self.h)):
            for x in xrange(max(len(frame[y]), self.w)):
                self[ (x, y) ] = frame[y][x]

    def push_frame(self, frame):
        """
        Push a frame to the screen
        """
        self.load_frame(frame)
        self.push()

    def __iter__(self):
        return LedScreenIterator(self)

class LedScreenIterator(object):
    def __init__(ls):
        pass

if __name__ == '__main__':
    screen = LedScreen()

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()
