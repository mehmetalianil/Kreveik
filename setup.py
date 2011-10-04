from setuptools import setup, find_packages

setup(
    name = "Kreveik",
    version = "0.5.2 dev",
    packages = find_packages(),
    # scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Mehmet Ali Anil",
    author_email = "mehmet.ali.anil@ieee.org",
    description = "Kreveik is a Python module for Boolean networks. With Kreveik, one can create, investigate dynamics of, form families of random Boolean networks.",
    license = "LICENSE.txt",
    keywords = "random boolean networks genetic algorithm",
    url = "http://github.com/mehmetalianil/Kreveik/",    
    # project home page, if any

    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
	  'Intended Audience :: Science/Research',
          'License :: Other/Proprietary License',
	  'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Physics'
          ],

)
