
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

import numpy as num 
import logging

def random_killer(ensemble,times):
    logging.info("Killing "+str(times)+" individuals")
    for i in range(times):
        randomnum = num.random.randint(0,len(ensemble))
        logging.info("("+str(i)+"/"+str(times)+") Killing "+str(ensemble[randomnum]))
        ensemble.remove(randomnum)
    
def qualified_killer(ensemble,**kwargs):
    pass

def underachiever_killer(ensemble,**kwargs):
    pass

    