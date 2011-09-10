import numpy as num

class probeable_obj (object):
    def __init__ (self):
        self.probes = []
    def attach (self,probe):
        if probe in self.probes:
            print "This probe is already attached."
        else:
            self.probes.append(probe)
    
    def populate_probes (self,subroutine):
        for probe in self.probe:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                num.append(probe.data,measured)
