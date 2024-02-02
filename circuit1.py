
import schemdraw
import schemdraw.elements as elm

# Create a new drawing
d = schemdraw.Drawing()

# Adding a general source to represent the pulse generator
pulse_gen = d.add(elm.SourceV().label('40 Hz\nPulse\nGenerator'))

# Adding a variable resistor (potentiometer) for LED brightness control
led_var_resistor = d.add(elm.Potentiometer().right().label('Brightness\nControl'))
led = d.add(elm.LED().right().label('LED'))

# Going back to the pulse generator to branch out for the piezo element
d.add(elm.Line().at(pulse_gen.start))
d.add(elm.Line().down().length(1.5))
piezo_var_resistor = d.add(elm.Potentiometer().right().label('Loudness\nControl'))
piezo = d.add(elm.Speaker().right().label('Piezo'))

# Drawing the connections
d.draw()

# Display the circuit diagram
d 
