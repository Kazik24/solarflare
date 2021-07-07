from solarflare.model import Model;
from solarflare.basic import Source,Delay,Monitor,Coupler;
import math
import matplotlib.pyplot as plt


model = Model(math.pi/64);

#optical ring resonator
#
#            __delay__
#           /         \
#           |         |
#           \_coupler_/
# Source >> /         \ >> Monitor


source = Source(1)
coupler = Coupler(math.pi*2,ballanceFactor=0.5)
delay = Delay(math.pi*2)
monitor = Monitor()

source.out % coupler.inp1
delay.inp % coupler.out2
delay.out % coupler.inp2
monitor.inp % coupler.out1

'''
coupler = Coupler(math.pi*2,ballanceFactor=0.5)
Source(1).out % coupler.inp1
Source(1).out % coupler.inp2
monitor = Monitor()
coupler.out1 % monitor.inp
'''

model.compile(monitor)

model.tick_phase(math.pi*80)

plt.plot(monitor.x_axis_ang,monitor.y_axis,color='green')
plt.show()