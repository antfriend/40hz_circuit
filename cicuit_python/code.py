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
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False)

# Base colors for main and opposite
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def blend_colors(color1, color2, phase):
    return (
        int(color1[0] + (color2[0] - color1[0]) * phase),
        int(color1[1] + (color2[1] - color1[1]) * phase),
        int(color1[2] + (color2[2] - color1[2]) * phase)
    )

# Instead of instantly toggling dominant color, use a phase to transition:
color_phase = 0.0
phase_direction = 1  # 1 means heading towards green, -1 means heading towards red
transition_frames = 40  # how many frames to fully transition between colors

resonance_frequency = 0
direction = 1
max_state = random.randint(2,4)

frame_count = 0
switch_interval = 80  # after 80 frames, reverse direction of phase
vertical_offset = 0
cycle_start_time = time.monotonic()
black_interval = 10

while True:
    now = time.monotonic()
    # Every 10 seconds, go black for 1 second
    if now - cycle_start_time >= black_interval:
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(1)
        cycle_start_time = time.monotonic()

    # Update the color_phase gradually
    # Each frame, move color_phase slightly
    color_phase += phase_direction * (1.0 / transition_frames)
    # Clamp the phase between 0 and 1
    if color_phase > 1.0:
        color_phase = 1.0
        phase_direction = -1  # start heading back to red
    elif color_phase < 0.0:
        color_phase = 0.0
        phase_direction = 1   # start heading back to green

    # Occasionally pick a new max_state
    if random.random() < 0.01:
        max_state = random.randint(2,4)

    resonator = resonate_range[resonance_frequency]

    # Adjust brightness (0.1 to 0.5)
    base_brightness = 0.1 + (resonance_frequency / (len(resonate_range)-1)) * 0.4
    pixels.brightness = base_brightness

    # Determine main and opposite color from the phase
    # When color_phase = 0 => mainly red, opposite green
    # When color_phase = 1 => mainly green, opposite red
    main_base_color = blend_colors(RED, GREEN, color_phase)
    opposite_base_color = blend_colors(GREEN, RED, color_phase)

    new_frame = []
    for row in range(5):
        for col in range(5):
            source_row = (row + vertical_offset) % 5
            val = resonator[source_row*5 + col]

            # Flicker: randomly vary brightness a bit
            def flicker(color):
                factor = random.uniform(0.8, 1.0)
                return (int(color[0]*factor), int(color[1]*factor), int(color[2]*factor))

            if val == 1:
                # Mostly main color with occasional opposite spark
                color = flicker(main_base_color)
                if random.randint(1, 20) == 1:
                    color = flicker(opposite_base_color)
            else:
                # Mostly opposite color with occasional main spark
                color = flicker(opposite_base_color)
                if random.randint(1, 20) == 1:
                    color = flicker(main_base_color)

            new_frame.append(color)

    # Display each frame multiple times to slow down framerate
    for _ in range(3):
        pixels[:] = new_frame
        pixels.show()
        time.sleep(random.uniform(0.2, 0.4))

    # Update resonance pattern
    resonance_frequency += direction
    if direction == 1 and resonance_frequency > max_state:
        resonance_frequency = max_state - 1
        direction = -1
    elif direction == -1 and resonance_frequency < 0:
        resonance_frequency = 1
        direction = 1

    frame_count += 1
    vertical_offset += 1