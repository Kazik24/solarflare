# SolarFlare - Linear optics simulator

Linear optics simulator intended for building simple light processing circuit models and
exploring wave propagation.

Project was created as a learning experience and for verifying simple mental models of
light processing systems.

#### Available elements
* Source - wave source with single primary harmonic and any number of side harmonics.
* Delay - delay line, can represent a waveguide and model its delay and losses.
* Coupler - optical coupler with two inputs, two outputs and adjustable coupling factor.
* Splitter - similar to coupler but has only one input and splits it to two outputs.
* Monitor - consumes any waves and saves it for plotting (accessed by x_axis/y_axis properties).

Element ports can be connected by `%` operator like this: `source.out % monitor.inp`.<br>
All elements are bidirectional which means that waves can propagate not only from input to output, but
also from output to input. Each element also has specified non-zero delay that is measured in radians
(2*pi means single wavelength).

#### Example
Creating optical ring resonator:
```
from solarflare.model import Model;
from solarflare.basic import Source,Delay,Monitor,Coupler;
import math
import matplotlib.pyplot as plt

#optical ring resonator
#
#            __delay__
#           /         \
#           |         |
#           \_coupler_/
# Source >> /         \ >> Monitor

#elements
source = Source(1)
coupler = Coupler(math.pi*2,ballanceFactor=0.5)
delay = Delay(math.pi*2)
monitor = Monitor()

#connect circuit
source.out % coupler.inp1
delay.inp % coupler.out2
delay.out % coupler.inp2
monitor.inp % coupler.out1

model = Model(math.pi/64) #create model with desired resolution
model.compile(monitor) #compile model (argument is any node)

model.tick_phase(math.pi*80) #fast forward 40 periods

#plot output recorded by monitor
plt.plot(monitor.x_axis_ang,monitor.y_axis,color='green')
plt.show()
```