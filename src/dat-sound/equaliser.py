import asyncore
import os, socket, json

import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../net'))
import ledremote

import random

import sync

s = ledremote.RemoteLedScreen('10.68.0.11', 8000)
metronome = sync.Metronome(fps=2.)
metronome.start()

def equaliser(dat):
    for x in range(12):
        for y in range(dat[x]):
            s[x, y] = 200, 100, 100

def clean():
    for y in range(10):
        for x in range(12):
            s[x, y] = 0, 0, 0

while True:
    dat = [random.randint(0, 10) for x in range(12)]
    clean()
    equaliser(dat)
    s.push()
    metronome.sync()
