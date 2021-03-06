import pyaudio
import numpy as np
import aubio
import os

import pygame
import pygame.gfxdraw
import random

from threading import Thread

import queue
import time
import math
import argparse

import circle_drawing
import snake
import line

parser = argparse.ArgumentParser()
parser.add_argument("-input", required=False, type=int, help="Audio Input Device")
args = parser.parse_args()

if args.input is None:
    print("No input device specified. Printing list of input devices now: ")
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print("Device number (%i): %s" % (i, p.get_device_info_by_index(i).get("name")))
    print(
        "Run this program with -input 1, or the number of the input you'd like to use."
    )
    exit()

pygame.init()

print(pygame.display.Info())

info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

# initialise pyaudio
p = pyaudio.PyAudio()

clock = pygame.time.Clock()

time.sleep(1)

# open stream

buffer_size = 512  # needed to change this to get undistorted audio
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(
    format=pyaudio_format,
    channels=n_channels,
    rate=samplerate,
    input=True,
    input_device_index=args.input,
    frames_per_buffer=buffer_size,
)

time.sleep(1)

# setup onset detector
tolerance = 0.3
win_s = 512  # fft size
hop_s = buffer_size // 2  # hop size
onset = aubio.onset("default", win_s, hop_s, samplerate)
# onset.set_threshold(0.5)
onset.set_minioi_ms(450)
# onset.set_delay(100)

q = queue.Queue()
low_pass = 0
magnitude = 0

input_q = queue.Queue()

apps = [line.Line(), snake.Snake(), circle_drawing.CircleDrawing()]
active_app_index = 2

black = (0, 0, 0)

for app in apps:
    app.setup(screen, None)


def draw_pygame():
    global active_app_index
    running = True
    delta_time = 0

    while running:
        key = pygame.key.get_pressed()

        if key[pygame.K_q]:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                active_app_index = (active_app_index + 1) % len(apps)
                screen.fill(black)
                pygame.display.flip()

        onset = not q.empty()
        if onset:
            b = q.get()

        apps[active_app_index].draw(
            screen,
            {
                "onset": onset,
                "low_pass": low_pass,
                "magnitude": magnitude,
                "delta_time": delta_time,
            },
        )
        delta_time = clock.tick(30)


def filter(signal, cut_off_frequency):
    freq_ratio = cut_off_frequency / samplerate
    window_size = int(math.sqrt(0.196196 + freq_ratio ** 2) / freq_ratio)
    cumsum = np.cumsum(np.insert(signal, 0, 0))
    filtered_signal = (cumsum[window_size:] - cumsum[:-window_size]) / window_size

    return np.linalg.norm(filtered_signal)


def get_onsets():
    while True:
        try:
            audiobuffer = stream.read(int(buffer_size / 2), exception_on_overflow=False)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)

            global magnitude
            magnitude = np.linalg.norm(signal) / 15

            global low_pass
            low_pass = filter(signal, 400.0) / 15

            if onset(signal):
                q.put(True)

        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            break


def getInput():
    while True:
        try:
            inputValue = input("Press W then enter to go to next app\n")
            input_q.put(inputValue)
        except KeyboardInterrupt:
            break


t = Thread(target=get_onsets, args=())
t.daemon = True
t.start()

input_thread = Thread(target=getInput, args=())
input_thread.daemon = True
input_thread.start()

draw_pygame()
stream.stop_stream()
stream.close()
pygame.display.quit()
