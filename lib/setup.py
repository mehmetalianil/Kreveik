from distutils.core import setup, Extension
import numpy

numpy_include = str(numpy.get_include())
module = Extension('boolfuncs_c', sources = ['boolfuncs.c'], include_dirs=[numpy_include])
setup(name = 'boolfuncs_c', version = '1.0', ext_modules = [module])

