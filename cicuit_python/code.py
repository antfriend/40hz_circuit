import time
import board
import neopixel
import random
import math

PIXEL_PIN = board.A3
NUM_PIXELS = 25
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=0.5, auto_write=False)

# Standalone colorwheel function (no rainbowio needed)
def colorwheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

# Parameters for the ripple effect
center_x = 2
center_y = 2
wave_frequency = 0.5
wave_speed = 0.02

frame_count = 0
vertical_offset = 0
repeat_frames = 1
frame_delay = (0.02, 0.04)

# Timings for fade cycle
normal_display_duration = 10.0  # seconds showing normal pattern
fade_duration = 1.0             # seconds to fade out and to fade in
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
    # 0 to normal_display_duration: full brightness
    # normal_display_duration to normal_display_duration+fade_duration: fade out
    # normal_display_duration+fade_duration to full_cycle: fade in
    if t_in_cycle < normal_display_duration:
        # Full brightness phase
        brightness_factor = 1.0
    elif t_in_cycle < normal_display_duration + fade_duration:
        # Fade out phase
        fade_progress = (t_in_cycle - normal_display_duration) / fade_duration
        brightness_factor = 1.0 - fade_progress
    else:
        # Fade in phase
        fade_progress = (t_in_cycle - (normal_display_duration + fade_duration)) / fade_duration
        brightness_factor = fade_progress

    # Base brightness for the effect (original code used up to 0.5)
    base_brightness = 0.5 * brightness_factor
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
        time.sleep(random.uniform(*frame_delay))

    frame_count += 1
    vertical_offset += 1
