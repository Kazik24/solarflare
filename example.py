from solarflare.model import Model;
from solarflare.basic import Source,Delay,Monitor,Coupler;
import math
import matplotlib.pyplot as plt
import numpy as np



#optical ring resonator
#
#            __delay__
#           /         \
#           |         |
#           \_coupler_/
# Source >> /         \ >> Monitor

model = Model(math.pi/64)

source = Source(1)
# change balance factor and see how efficient is ring resonator
coupler = Coupler(math.pi*2,ballanceFactor=0.25)
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

res = []
for mul in np.arange(0.6,1.4,0.01):
    model.reset()
    source.frequency_multipler = mul
    model.tick_phase(math.pi * 80)

    # plt.plot(monitor.x_axis_ang,monitor.y_axis,color='green')
    ampl = monitor.y_axis[monitor.x_axis > math.pi * 60].max()
    print(ampl)
    res.append(ampl)

plt.plot(res)
plt.show()
#vals = np.array(vals)
#plt.plot(vals[:,0],vals[:,1])
#plt.show()