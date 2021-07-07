

from solarflare.model import Model;
from solarflare.basic import Source,Delay,Monitor,Coupler;
import math
import matplotlib.pyplot as plt


model = Model(math.pi/64);

'''
#resonator
source = model.add(Source(1,0,1))
delaySig = model.add(Delay(math.pi*2,ratio=0.45))
monitor = model.add(Monitor())
coupler = model.add(Coupler(math.pi*2,ballanceFactor=0.5))

source.out % coupler.inp1
delaySig.inp % coupler.out2
delaySig.out % coupler.inp2
monitor.inp % coupler.out1
'''
coupler = Coupler(math.pi*2,ballanceFactor=0.5)
Source(1).out % coupler.inp1
Source(1).out % coupler.inp2
monitor = Monitor()
coupler.out1 % monitor.inp

model.compile(monitor)

model.tick_phase(math.pi*80)

plt.plot(monitor.x_axis_ang,monitor.y_axis,color='green',label='waveTop')
plt.show()