from distutils.core import setup

setup(
    name='Kreveik',
    version='0.5.0 dev',
    author='Mehmet Ali Anil',
    author_email='mehmet.ali.anil@ieee.org',
    packages=['kreveik', 'kreveik.test'],
    scripts=[],
    url='http://github.com/mehmetalianil/Kreveik/',
    license='LICENSE.txt',
    description='Kreveik is a Python module for Boolean networks. With Kreveik, one can build Boolean networks, create random Boolean networks, investigate dynamics of these networks, form families of them, investigate macroscopic variables and expose them to genetic algorithms.',
    long_description=open('README.txt').read(),
    install_requires=[
        "networkx >= 1.5",
        "numpy >= 1.5.1",
        "matplotlib >= 1.0.1"
    ],
)