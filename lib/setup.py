from distutils.core import setup, Extension
import numpy

numpy_include = str(numpy.get_include())
module = Extension('trace', sources = ['xor_masking.c'], include_dirs=[numpy_include])
setup(name = 'Trace Test', version = '1.0', ext_modules = [module])

