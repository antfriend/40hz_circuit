import time
import board
import neopixel
import random
import math

PIXEL_PIN = board.A3
NUM_PIXELS = 25
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.1, auto_write=False)

# Modified color function to produce shades of green and occasionally a bit of red
def colorwheel(pos):
    # pos in [0, 255]
    # We'll create a varying green using a sinusoidal pattern and occasionally insert a red pixel
    g = int((math.sin(pos * math.pi / 128) + 1) * 127.5)
    if random.random() < 0.01:
        return (255, 0, 0)  # Occasional red pixel
    return (0, g, 0)

# Parameters for the ripple effect
center_x = 2
center_y = 1
wave_frequency = 40
wave_speed = 0.42
delay_secs = 0.022

frame_count = 0
vertical_offset = 0
repeat_frames = 4


# Timings for fade cycle
normal_display_duration = 30.0  # seconds showing normal pattern
fade_duration = 0.1             # seconds to fade out and to fade in
full_cycle = normal_display_duration + fade_duration + fade_duration

cycle_start_time = time.monotonic()

def blur_frame(frame, width=5, height=5):
    blurred = [None]*(width*height)
    for row in range(height):
        for col in range(width):
            r_tot = 0
            g_tot = 0
            b_tot = 0
            count = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nr = row + dy
                    nc = col + dx
                    if 0 <= nr < height and 0 <= nc < width:
                        idx = nr*width + nc
                        r, g, b = frame[idx]
                        r_tot += r
                        g_tot += g
                        b_tot += b
                        count += 1
            blurred[row*width + col] = (r_tot//count, g_tot//count, b_tot//count)
    return blurred

while True:
    now = time.monotonic()
    t_in_cycle = (now - cycle_start_time) % full_cycle

    # Determine the brightness factor based on where we are in the cycle:
    if t_in_cycle < normal_display_duration:
        # Full brightness phase
        brightness_factor = 0.2
    elif t_in_cycle < normal_display_duration + fade_duration:
        # Fade out phase
        fade_progress = (t_in_cycle - normal_display_duration) / fade_duration
        brightness_factor = 0.2 - fade_progress
    else:
        # Fade in phase
        fade_progress = (t_in_cycle - (normal_display_duration + fade_duration)) / fade_duration
        brightness_factor = fade_progress

    base_brightness = 0.2 * brightness_factor
    pixels.brightness = base_brightness

    new_frame = []
    for row in range(5):
        for col in range(5):
            source_row = (row + vertical_offset) % 5
            dx = source_row - center_y
            dy = col - center_x
            distance = math.sqrt(dx*dx + dy*dy)

            wave = distance * wave_frequency - frame_count * wave_speed
            hue = int((math.sin(wave) + 1) * 127)
            color = colorwheel(hue)
            new_frame.append(color)

    blurred_frame = blur_frame(new_frame)

    for _ in range(repeat_frames):
        pixels[:] = blurred_frame
        pixels.show()
        time.sleep(delay_secs)

    frame_count += 1
    vertical_offset += 1
