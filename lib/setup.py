from distutils.core import setup, Extension

module = Extension('pr', sources = ['test.c'])
setup(name = 'Pr test', version = '1.0', ext_modules = [module])