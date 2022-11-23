# -*- coding: utf-8 -*-

from .model import Element;
import numpy as np;
import math;


class Source(Element):
    
    
    def __init__(self,amplitude,phaseShift=0.0,freqMultipler=1.0,sidef=None):
        Element.__init__(self,"out")
        if amplitude <= 0 or freqMultipler <= 0: raise ValueError();
        self._waves = [[float(amplitude),float(phaseShift),float(freqMultipler)]];
        if sidef is not None:
            side = [];
            for wave in list(sidef):
                if len(wave) != 3: raise ValueError("side frequencies must be 3 element collection")
                side.append(tuple([float(wave[0]),float(wave[1]),float(wave[2])]))
            self._waves.extend(side)
    @property
    def amplitude(self):
        return self._waves[0][0]
    @amplitude.setter
    def amplitude(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError()
        self._waves[0][0] = value
    @property
    def phase_shift(self):
        return self._waves[0][1]
    @phase_shift.setter
    def phase_shift(self, value):
        self._waves[0][1] = float(value)
    @property
    def frequency_multipler(self):
        return self._waves[0][2]
    @frequency_multipler.setter
    def frequency_multipler(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError()
        self._waves[0][2] = value
    @property
    def out(self):
        return self.get_bond("out");
    def _calcOutputs(self,currentTick,currentPhase):
        val = 0;
        for w in self._waves:
            val += w[0]*math.sin((currentPhase+w[1])*w[2])
        self._set_output("out",val)
    def _acceptInputs(self,currentTick,currentPhase):
        pass


class Delay(Element):
    
    
    def __init__(self,phaseDelay,ratio=1.0):
        Element.__init__(self,"inp","out")
        if phaseDelay <= 0 or ratio < 0: raise ValueError();
        self._phaseDelayExact = float(phaseDelay);
        self._ratio = float(ratio)
        self._forward = None;
        self._backward = None;
        self._forwardIdx = 0;
        self._backwardIdx = 0;
        
    @property
    def out(self):
        return self.get_bond("out");
    @property
    def inp(self):
        return self.get_bond("inp");
    def reset(self):
        if self._forward is not None: self._forward.fill(0);
        if self._backward is not None: self._backward.fill(0);
        self._forwardIdx = 0;
        self._backwardIdx = 0;
    def _reset_elem(self):
        self.reset()
    @property
    def power_factor(self):
        return self._ratio;
    def _register(self,model):
        steps = int(max(round(self._phaseDelayExact/model.phase_inc),1));
        self._forward = np.zeros(steps,dtype='float64');
        self._backward = np.zeros(steps,dtype='float64');
        self._forwardIdx = 0;
        self._backwardIdx = 0;
    def _calcOutputs(self,currentTick,currentPhase):
        self._set_output("out",self._forward[self._forwardIdx]*self._ratio)
        self._set_output("inp",self._backward[self._backwardIdx]*self._ratio)
    def _acceptInputs(self,currentTick,currentPhase):
        self._forward[self._forwardIdx] = self._get_input("inp")
        self._backward[self._backwardIdx] = self._get_input("out")
        self._forwardIdx = (self._forwardIdx + 1) % len(self._forward)
        self._backwardIdx = (self._backwardIdx + 1) % len(self._backward)
        
class Monitor(Element):
    def __init__(self,maxPoints=10000):
        Element.__init__(self,"inp")
        self._maxPoints = int(max(maxPoints,2));
        self._xAxis = []
        self._yAxis = []
    @property
    def inp(self):
        return self.get_bond("inp")
    @property
    def x_axis(self):
        return np.array(self._xAxis)
    @property
    def y_axis(self):
        return np.array(self._yAxis)
    @property
    def x_axis_ang(self):
        return np.rad2deg(self._xAxis)
    @property
    def points(self):
        return np.array([self.x_axis,self.y_axis]).transpose()
    @property
    def points_ang(self):
        return np.array([self.x_axis_ang,self.y_axis]).transpose()
    def clear(self):
        self._xAxis.clear()
        self._yAxis.clear()
    def _reset_elem(self):
        self.clear()
    def _calcOutputs(self,currentTick,currentPhase):
        pass
    def _acceptInputs(self,currentTick,currentPhase):
        if len(self._yAxis) >= self._maxPoints:
            del self._xAxis[0]
            del self._yAxis[0]
        self._xAxis.append(currentPhase)
        self._yAxis.append(self._get_input("inp"))

class Coupler(Element):
    
    def __init__(self,phaseDelay,ballanceFactor=0.5,ratio1=1,ratio2=1):
        Element.__init__(self,"inp1","inp2","out1","out2")
        if phaseDelay <= 0 or ratio1 < 0 or ratio2 < 0: raise ValueError();
        self._phaseDelayExact = float(phaseDelay);
        self._ballance = max(min(1,float(ballanceFactor)),0)
        self._ratio1 = float(ratio1)
        self._ratio2 = float(ratio2)
        self._forward1 = None;
        self._forward2 = None;
        self._backward1 = None;
        self._backward2 = None;
        self._forwardIdx1 = 0;
        self._forwardIdx2 = 0;
        self._backwardIdx1 = 0;
        self._backwardIdx2 = 0;
    def reset(self):
        if self._forward1 is not None: self._forward1.fill(0);
        if self._forward2 is not None: self._forward2.fill(0);
        if self._backward1 is not None: self._backward1.fill(0);
        if self._backward2 is not None: self._backward2.fill(0);
        self._forwardIdx1 = 0;
        self._forwardIdx2 = 0;
        self._backwardIdx1 = 0;
        self._backwardIdx2 = 0;
    def _reset_elem(self):
        self.reset()
    @property
    def out1(self):
        return self.get_bond("out1");
    @property
    def out2(self):
        return self.get_bond("out2");
    @property
    def inp1(self):
        return self.get_bond("inp1");
    @property
    def inp2(self):
        return self.get_bond("inp2");
    @property
    def power_factor(self):
        return (self._ratio1+self._ratio2)/2;
    def _register(self,model):
        steps = int(max(round(self._phaseDelayExact/model.phase_inc),1));
        self._forward1 = np.zeros(steps,dtype='float64');
        self._forward2 = np.zeros(steps,dtype='float64');
        self._backward1 = np.zeros(steps,dtype='float64');
        self._backward2 = np.zeros(steps,dtype='float64');
        self._forwardIdx1 = 0;
        self._forwardIdx2 = 0;
        self._backwardIdx1 = 0;
        self._backwardIdx2 = 0;
    def _calcOutputs(self,currentTick,currentPhase):
        fw1 = self._forward1[self._forwardIdx1]*self._ballance +\
              self._forward2[self._forwardIdx2]*(1-self._ballance)
        fw2 = self._forward1[self._forwardIdx1]*(1-self._ballance) +\
              self._forward2[self._forwardIdx2]*self._ballance
        bw1 = self._backward1[self._backwardIdx1]*self._ballance +\
              self._backward2[self._backwardIdx2]*(1-self._ballance)
        bw2 = self._backward1[self._backwardIdx1]*(1-self._ballance) +\
              self._backward2[self._backwardIdx2]*self._ballance
        self._set_output("out1",fw1*self._ratio1)
        self._set_output("out2",fw2*self._ratio2)
        self._set_output("inp1",bw1*self._ratio1)
        self._set_output("inp1",bw2*self._ratio2)
    def _acceptInputs(self,currentTick,currentPhase):
        self._forward1[self._forwardIdx1] = self._get_input("inp1")
        self._forward2[self._forwardIdx2] = self._get_input("inp2")
        self._backward1[self._backwardIdx1] = self._get_input("out1")
        self._backward1[self._backwardIdx2] = self._get_input("out2")
        self._forwardIdx1 = (self._forwardIdx1 + 1) % len(self._forward1)
        self._forwardIdx2 = (self._forwardIdx2 + 1) % len(self._forward2)
        self._backwardIdx1 = (self._backwardIdx1 + 1) % len(self._backward1)
        self._backwardIdx2 = (self._backwardIdx2 + 1) % len(self._backward2)
        
class Splitter(Element):
    def __init__(self,phaseDelay,ratio1=1,ratio2=1):
        raise ValueError("not implemented")
        Element.__init__(self,"inp1","inp2","out")
        if phaseDelay <= 0 or ratio1 < 0 or ratio2 < 0: raise ValueError();
        self._phaseDelayExact = float(phaseDelay);
        self._ratio1 = float(ratio1)
        self._ratio2 = float(ratio2)
        self._forward = None;
        self._backward = None;
        self._forwardIdx = 0;
        self._backwardIdx = 0;
    @property
    def out(self):
        return self.get_bond("out");
    @property
    def inp1(self):
        return self.get_bond("inp1");
    @property
    def inp2(self):
        return self.get_bond("inp2");
    def reset(self):
        if self._forward is not None: self._forward.fill(0);
        if self._backward is not None: self._backward.fill(0);
        self._forwardIdx = 0;
        self._backwardIdx = 0;
    def _reset_elem(self):
        self.reset()
    @property
    def power_factor(self):
        return (self._ratio1+self._ratio2)/2;
    def _register(self,model):
        steps = int(max(round(self._phaseDelayExact/model.phase_inc),1));
        self._forward = np.zeros(steps,dtype='float64');
        self._backward = np.zeros(steps,dtype='float64');
        self._forwardIdx = 0;
        self._backwardIdx = 0;
    def _calcOutputs(self,currentTick,currentPhase):
        self._set_output("out",self._forward[self._forwardIdx])
        self._set_output("inp1",self._backward[self._backwardIdx]*self._ratio1*0.5)
        self._set_output("inp2",self._backward[self._backwardIdx]*self._ratio2*0.5)
    def _acceptInputs(self,currentTick,currentPhase):
        fw = self._get_input("inp1")*self._ratio1 + self._get_input("inp2")*self._ratio2
        self._forward[self._forwardIdx] = fw
        self._backward[self._backwardIdx] = self._get_input("out")
        self._forwardIdx = (self._forwardIdx + 1) % len(self._forward)
        self._backwardIdx = (self._backwardIdx + 1) % len(self._backward)
    
    