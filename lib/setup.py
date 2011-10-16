from distutils.core import setup, Extension
import numpy

numpy_include = str(numpy.get_include())
module = Extension('xor_masking', sources = ['xor_masking.c'], include_dirs=[numpy_include])
setup(name = 'XOR Masking', version = '1.0', ext_modules = [module])

