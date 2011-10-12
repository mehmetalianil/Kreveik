from distutils.core import setup, Extension
import numpy


INC_DIRS = ['../']
INC_DIRS.insert(0,numpy.get_include()) 
module = Extension('trace', sources = ['xor_masking.c'])
setup(name = 'Trace Test', version = '1.0', ext_modules = [module])