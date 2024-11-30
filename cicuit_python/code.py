import time
import board
import neopixel

from displayio import Bitmap
from rainbowio import colorwheel

resonate_1 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
]

resonate_2 = [
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,1,1,0,
    0,0,1,0,0,
    0,0,0,0,0,
]

resonate_3 = [
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,1,1,1,
    0,1,1,1,0,
    0,0,1,0,0,
]

resonate_4 = [
    1,1,1,1,1,
    1,1,1,1,1,
    1,1,1,1,1,
    1,1,1,1,1,
    1,1,1,1,1,
]

resonate_range = [resonate_1, resonate_2, resonate_3, resonate_4]
resonance_frequency = 0  # Start at the beginning
direction = 1  # 1 for forward, -1 for backward

pixels = neopixel.NeoPixel(board.A3, 5 * 5, brightness=0.05, auto_write=False)

while True:
    resonator = resonate_range[resonance_frequency]

    # Adjust brightness dynamically based on the index
    brightness = (resonance_frequency + 1) / len(resonate_range)  # Scale between 0.25 and 1
    pixels.brightness = brightness
    
    for hue in range(0, 255, 3):
        color = colorwheel(hue)
        pixels[:] = [pixel * color for pixel in resonator]
        pixels.show()
        
        # Apply the duty cycle: ON time (3 ms)
        time.sleep(0.003)
        
        # Turn off LEDs: OFF time (22 ms)
        pixels.fill(0)
        pixels.show()
        time.sleep(0.022)
    
    # Update the resonance frequency
    resonance_frequency += direction
    if resonance_frequency >= len(resonate_range):  # If at the end, reverse direction
        resonance_frequency = len(resonate_range) - 2  # Step back into range
        direction = -1
    elif resonance_frequency < 0:  # If at the beginning, reverse direction
        resonance_frequency = 1  # Step forward into range
        direction = 1
