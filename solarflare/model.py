
import math;




class Model:
    
    
    def __init__(self,phaseTick):
        if phaseTick <= 0: raise ValueError("phase tick must be positive");
        self._phaseTick = float(phaseTick);
        self._tickCount = -1;
        self._tickables = [];
    
    def add(self,element):
        if not isinstance(element,Element): raise ValueError("expected Element instance");
        if element in self._tickables: raise ValueError("already present");
        self._tickables.append(element);
        element._model = self;
        element._register(self);
        return element;
    def canAdd(self,element):
        if not isinstance(element,Element): return False;
        if element in self._tickables: return False;
        return True;
    @property
    def current_tick(self):
        return self._tickCount;
    @property
    def phase_inc(self):
        return self._phaseTick;
    @property
    def current_phase(self):
        return max(0,self._phaseTick*self._tickCount);
    def remove(self,element):
        if not isinstance(element,Element): raise ValueError("expected Element instance");
        if element in self._tickables and element._model == self:
            self._tickables.remove(element)
            element._model = None;
    def tick_phase(self,phase):
        self.tick(int(max(round(float(phase)/self._phaseTick),1)))
    def tick(self,count=1):
        for i in range(int(count)):
            ticks = self._tickCount;
            ticks += 1;
            self._tickCount = ticks;
            phase = ticks * self._phaseTick;
            for e in self._tickables:
                e._calcOutputs(ticks,phase);
            for e in self._tickables:
                e._acceptInputs(ticks,phase);
        pass
    pass

    def compile(self,anyNode):
        toScan = [];
        if anyNode is not None: toScan.append(anyNode)
        while(len(toScan) > 0):
            n = toScan[0];
            #print("scanning: ",type(n))
            del toScan[0];
            if self.canAdd(n):
                self.add(n);
                for (name,bond) in n._bonds.items():
                    cn = bond.connection
                    if cn is not None: toScan.append(cn._element)
        pass
            
            
        
        
        

class Bond:
    
    
    def __init__(self,name,element):
        if name is None: raise ValueError("null argument");
        self._name = str(name);
        self._element = element;
        self._connection = None;
        self._output = 0.0;
    
    @property
    def is_connected(self):
        return self._connection is not None;
    @property
    def connection(self):
        return self._connection;
    @property
    def name(self):
        return self._name;
    @property
    def value(self):
        return float(self._output);
    
    def __mod__(self,other):
        self.link(other);
    
    def unlink(self):
        if self._connection is not None:
            self._connection._connection = None;
            self._connection = None;
    
    def link(self,target):
        if not isinstance(target,Bond): raise ValueError("not instance of Bond");
        self._connection = target;
        target._connection = self;
        
class Element:
    
    
    
    def __init__(self,*names):
        self._bonds = {};
        self._model = None;
        for s in names:
            s = str(s)
            self._bonds[s] = Bond(s,self);
        
    def get_bond(self,name) -> Bond:
        name = str(name)
        if name not in self._bonds: raise ValueError("unknown bond name: "+name);
        b = self._bonds[name];
        if not isinstance(b,Bond): raise TypeError("bad type");
        return b;
        
    def _get_input(self,name):
        b = self.get_bond(name);
        c = b._connection;
        if c is None: return 0.0;
        return c.value;
    @property
    def power_factor(self):
        return math.nan;
    def _set_output(self,name,value):
        self.get_bond(name)._output = float(value);
    
    def _register(self,model):
        pass
    def _calcOutputs(self,currentTick,currentPhase):
        pass
    def _acceptInputs(self,currentTick,currentPhase):
        pass
    