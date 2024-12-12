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
    0,1,1,1,0,
    0,1,1,1,0,
    0,1,1,1,0,
    0,1,1,1,0,
    0,1,1,0,0,
]

resonate_range = [resonate_1, resonate_2, resonate_3, resonate_4]

PIXEL_PIN = board.A3
NUM_PIXELS = 25
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.05, auto_write=False)

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
max_state = random.randint(2,4)

dominant_color = 'red'
frame_count = 0
switch_interval = 40  # switch dominant color every ~40 frames

vertical_offset = 0  # used to scroll the image upwards

cycle_start_time = time.monotonic()  # track time to go black every 10 seconds
black_interval = 10  # seconds

while True:
    now = time.monotonic()
    # Every 10 seconds, go black for 1 second
    if now - cycle_start_time >= black_interval:
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(1)
        cycle_start_time = time.monotonic()  # reset the timer after blackout

    # Every switch_interval frames, toggle the dominant color
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
    # Construct the frame with vertical scrolling
    for row in range(5):
        for col in range(5):
            # Compute the source row with vertical offset
            source_row = (row + vertical_offset) % 5
            val = resonator[source_row*5 + col]

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

    # Faster cycling: shorter delay
    time.sleep(random.uniform(0.05, 0.3))

    # Update the resonance pattern index
    resonance_frequency += direction

    # If going up and surpass max_state, reverse direction
    if direction == 1 and resonance_frequency > max_state:
        resonance_frequency = max_state - 1
        direction = -1

    # If going down and below 0, reverse direction
    elif direction == -1 and resonance_frequency < 0:
        resonance_frequency = 1
        direction = 1

    frame_count += 1
    vertical_offset += 1  # Scroll the image upwards each frame