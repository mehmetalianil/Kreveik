import numpy
import trace
a = numpy.eye(6)==1
b = numpy.eye(6)!=1
c = (numpy.eye(6)==1)[1,:]

trace.trace(a,b,c)