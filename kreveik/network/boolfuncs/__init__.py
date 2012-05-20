
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
For a network, every single node is taken, its mask and state vector is clipped.
They are subject to a boolean operation from numpy libraries.
Then from the fact that whether the node outputs a number greater than the 
shortened state vector, the node outputs 1 or 0.
These values are gathered up and outputted as a new state vector.
The method can be:
    num.logical_or
    num.logical_and
    num.logical_xor
    num.logical_xnor
    
    or any other function that outputs an integer with an input of two ndarrays.        
"""

from boolfuncs import xor_masking, and_masking, or_masking, xor_masking_C, and_masking_C, or_masking_C



