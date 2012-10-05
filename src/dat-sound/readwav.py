
import wave
import numpy as np
from numpy import fft

x = wave.open('kiri.wav')

offset = x._file.file.tell()
channels = x.getnchannels()
frames = x.getnframes()

wave = np.memmap(x._file.file, dtype=np.int16, mode='r',
    offset=offset, shape=(frames, channels))

def nx_pow2(x):
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    x += 1

    return x

# fps must be power of 2
def get_eql(pos, fps):
    #fps = nx_pow2(fps)
    cs = nx_pow2(44100 / fps)
    chunk = np.real(fft.fft(wave[pos:pos+cs, 0], axis=0)) / 32768.0
    eql = np.sum(np.reshape(chunk, (-1, (cs / 16))), axis=1)
    eql /= (cs / 16)
    
    eql -= np.min(eql)
    eql /= 2
    eql = np.minimum(1, eql)

    eql *= 10
    reql = np.array(eql, dtype=int)

    return reql

