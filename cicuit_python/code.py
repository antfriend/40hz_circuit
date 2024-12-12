import time
import board
import neopixel
import random

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

PIXEL_PIN = board.A3
NUM_PIXELS = 25
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.05, auto_write=False)

# Flicker color functions
def random_red():
    factor = random.uniform(0.2, 1.0)
    return (int(255*factor), 0, 0)

def random_green():
    factor = random.uniform(0.2, 1.0)
    return (0, int(255*factor), 0)

def black():
    return (0, 0, 0)

resonance_frequency = 0
direction = 1

# Start with a random max_state
max_state = random.randint(2,4)

# Start with red as dominant color
dominant_color = 'red'
frame_count = 0
switch_interval = 40  # switch dominant color every ~40 frames

while True:
    # Every 'switch_interval' frames, toggle the dominant color
    if frame_count % switch_interval == 0:
        dominant_color = 'green' if dominant_color == 'red' else 'red'
        
        # Occasionally pick a new max_state
        if random.random() < 0.3:
            max_state = random.randint(2,4)

    resonator = resonate_range[resonance_frequency]

    # Adjust brightness (0.1 to 0.5)
    base_brightness = 0.1 + (resonance_frequency / (len(resonate_range)-1)) * 0.4
    pixels.brightness = base_brightness

    new_frame = []
    for val in resonator:
        if val == 1:
            if dominant_color == 'red':
                color = random_red()
                # Occasional green spark
                if random.randint(1, 15) == 1:
                    color = random_green()
            else:
                color = random_green()
                # Occasional red spark
                if random.randint(1, 15) == 1:
                    color = random_red()
        else:
            color = black()
        new_frame.append(color)

    pixels[:] = new_frame
    pixels.show()

    # Slow down the cycle
    time.sleep(random.uniform(0.2, 0.4))

    # Update resonance frequency for next cycle
    resonance_frequency += direction

    # If going up and surpass max_state, reverse direction
    if direction == 1 and resonance_frequency > max_state:
        resonance_frequency = max_state - 1
        direction = -1

    # If going down and go below 0, reverse direction
    elif direction == -1 and resonance_frequency < 0:
        resonance_frequency = 1
        direction = 1

    frame_count += 1
