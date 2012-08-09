
#    Copyright 2012 Mehmet Ali ANIL
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#    http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Kreveik
=======

Kreveik is a Python project that is meant to provide a codebase for research about evolution 
and dynamics of random boolean networks (RBNs).

Kreveik provides: 
    * Class definitions concerning Boolean Networks (BNs) an ensembles of them. 
    * Tools for working on and visualizing Boolean Networks.
    * Tools concerning Genetic Algorithms (GAs), such as mutations, fitness functions.
    * Tools enabling data extraction from processes such as Genetic Algorithms.
    * Tools for motif frequency analysis.

Available Subpackages
---------------------
classes
    class definitions used throughout the code.
        
family
    tools for creating and manipulating families, i.e. ensembles of networks

network
    tools for creating and manipulating networks.
    
probes
    probes, which are data extracting objects, for further data analysis.

genetic
    tools and functions concerning genetic algorithms in general.

"""

import classes
import family
import genetic
import network
import probes

import logging
logging.basicConfig(level=logging.INFO)

__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil","Ayse Erzan","Burcin Danaci"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "mehmet.anil@colorado.edu"
__status__ = "Production"

defaults = {}
defaults["type_list"]  = [classes.Family, classes.Motif, classes.Network]

#
#
#  TODO !!! mehmet.ali.anil
#
#def save(filename, objects=[], **kwargs):
#    """
#    Saves the current state of the experiment.
#    """
#    import shelve
#    import os
#    import logging
#    
#    if "ext" in kwargs:
#        ext = kwargs["ext"]
#    else:    
#        ext = ".kvk"
#        
#    if "type_list" in kwargs:
#        type_list = kwargs["typelist"]
#    else:
#        type_list = defaults["type_list"]    
#    
#    if "type_list" in kwargs:
#        extras = kwargs["extras"]
#    else:
#        extras = []
#        
#    filename = filename+ext
#    
#    if os.path.isfile(filename):
#        logging.info("The file"+filename+"is already present.")
#        logging.info("Actions:")
#        logging.info("(O)verwrite")
#        logging.info("(N)ew filename")
#        logging.info("e(X)it")
#        prompt = raw_input("Please select action:")
#        
#        while not(prompt in "ONXonx"):
#            logging.info("(O)verwrite")
#            logging.info("(N)ew filename")
#            logging.info("e(X)it")
#            logging.info("Please select a valid action by typing O,N or X.")
#            prompt = raw_input("Please select action:")
#            
#        if prompt == "X" or prompt == "x":
#            logging.info("Exiting saving sequence.")
#            return None
#        elif prompt == "O" or prompt == "o":
#            logging.info("Overwriting"+filename+".")
#        elif prompt == "N" or prompt == "n":
#            logging.info("Enter new filename without extension .kvk:")
#            raw_input("Filename :")
#            filename = filename+ext
#        else:
#            logging.debug("Saving sequence failed.")
#            return None
#        
#    theshelve = shelve.open(filename)
#    
#    save_list = []
#    globals_copy = globals().copy()
#    logging.debug("Copy of the locals():")
#    logging.debug(str(globals_copy))
#    
#    for item in globals_copy:
#        logging.debug("Trying "+str(globals_copy[item]))
#        if type(globals_copy[item]) in type_list:
#            logging.debug(str(globals_copy[item])+", item #"+str(item)+", with the type "
#                          +str(type(globals_copy[item]))+" is added to the save_list.")
#            save_list.append([item,globals_copy[item],type(globals_copy[item])])
#        if globals_copy[item] in extras:
#            save_list.append([item,globals_copy[item],type(globals_copy[item])])
#            logging.debug(str(globals_copy[item])+", item #"+str(item)+", with the type "
#                          +str(type(globals_copy[item]))+" is added to the save_list.")
#    
#    logging.debug("The following list is generated for saving:")
#    logging.debug(str(save_list))
#    
#    if len(save_list) == 0:
#        logging.info("Unable to recognize an object to be saved. ")
#        logging.info("Please create networks, families and then try to save the present state.")
#        return None
#    else:
#        logging.info("The following objects are being saved:") 
#        for item in save_list:
#            logging.info("("+save_list[2]+")"+" "+save_list[1]) 
#        theshelve[save_list[0]] = save_list[1]
#    
#    theshelve.close()
#    logging.info("Saved as "+filename)    

