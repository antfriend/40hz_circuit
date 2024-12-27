import time
import board
import neopixel
import random

# --- Configuration ---
PIXEL_PIN = board.A3       # The pin the NeoPixels are connected to
NUM_PIXELS = 25            # Total number of NeoPixels in a 5x5 grid
BRIGHTNESS = 0.5           # Overall brightness of the LEDs (0.0 to 1.0)

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)

def crossfade_all_pixels(start_color, end_color, steps=50, delay=0.01):
    """
    Smoothly crossfades all pixels from start_color to end_color.
    
    :param start_color: (r, g, b) tuple representing the initial color
    :param end_color: (r, g, b) tuple representing the final color
    :param steps: Number of steps in the transition (higher means smoother)
    :param delay: Delay in seconds between each step
    """
    (r1, g1, b1) = start_color
    (r2, g2, b2) = end_color
    
    for i in range(steps + 1):
        # Calculate the intermediate color
        r = r1 + (r2 - r1) * i / steps
        g = g1 + (g2 - g1) * i / steps
        b = b1 + (b2 - b1) * i / steps
        
        pixels.brightness = BRIGHTNESS
        # Set the color to all pixels
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(0.02)
        pixels.brightness = 0
        pixels.show()
        time.sleep(delay - 0.02)
        

def get_random_color():
    """
    Returns a random (r, g, b) tuple.
    """
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255)
    )

def main():
    """
    Continuously crossfade between random colors on the 5x5 NeoPixel grid.
    """
    current_color = get_random_color()
    
    while True:
        next_color = get_random_color()
        steps = random.randint(45, 50)
        crossfade_all_pixels(current_color, next_color, steps, delay=0.025)
        current_color = next_color

# Run the main loop
if __name__ == "__main__":
    main()
