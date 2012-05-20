
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

import generators
import mutators
import scorers
import selectors
import boolfuncs


def global_clustering_out(network):
    """
    Returns the global clustering coefficient for output connections for every single node 
    """
    local_clustering_out(network).mean()

def global_clustering_in(network):
    """
    Returns the global clustering coefficient for input connections for every single node 
    """
    local_clustering_in(network).mean()
                