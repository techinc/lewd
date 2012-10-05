
import wave
import numpy as np
from numpy import fft

x = wave.open('kiri.wav')

offset = x._file.file.tell()
channels = x.getnchannels()
frames = x.getnframes()

wave = np.memmap(x._file.file, dtype=np.int16, mode='r',
    offset=offset, shape=(frames, channels))

