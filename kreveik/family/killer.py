
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
family.killer module
====================
Houses functions that kill a portion of a population.

Functions
---------
    random_killer: Kills randomly from an ensemble
    qualified_killer: TODO
    underachiever_killer: TODO
    
"""



def random_killer(ensemble,times):
    import numpy as num 
    import logging
    """
    Kills randomly from an ensemble
    
    Kills a number of random individuals disregarding any properties of them.
    
    Args:
    ----
        ensemble: An object of Ensemble type (probably a Family) in which 
        individuals will be randomly killed.
        
        times: the number of individuals that will be killed.
    
    Returns:
    --------
        None            
    """
    logging.info("Killing "+str(times)+" individuals")
    for i in range(times):
        randomnum = num.random.randint(0,len(ensemble))
        logging.info("("+str(i)+"/"+str(times)+") Killing "+str(ensemble[randomnum]))
        ensemble.remove(randomnum)
    
def qualified_killer(ensemble,**kwargs):
    pass

def underachiever_killer(ensemble,**kwargs):
    pass

__all__ = [random_killer, qualified_killer, underachiever_killer]