"""
Probable Class definition
"""
import numpy as num

class ProbeableObj (object):
    def __init__ (self):
        self.probes = []
    def attach (self,probe):
        if probe in self.probes:
            print "This probe is already attached."
        else:
            self.probes.append(probe)
    
    def populate_probes (self,subroutine):
        for probe in self.probes:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                probe.data = num.append(probe.data,measured)
                