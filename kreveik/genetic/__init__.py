
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

def score(element,scorer=None):
    
    """
    If a scorer is specified, the score of the element calculated with that
    scorer is returned. 
    If scorer is not set, then the element is scored with the scorer specified 
    in its definition.
    """
    if scorer == None:
        element.score = element.scorer(element)
    else:
        return scorer(element)

def genetic_iteration(ensemble,**kwargs):
    import logging
    '''
    Runs one iteration of the genetic algorithm.
    It finds wildtypes of the family, mutates them, populates the family with mutants
    and assasinates as much of it has mutated. 
    '''
    if ((ensemble.scorer == None) or (ensemble.selector == None)
        or (ensemble.mutator == None) or (ensemble.killer == None)):
        raise ValueError("An element needs its scorer, killer, selector and mutator \
        defined in order to be fed into the GA")
        return False
    
    logging.info("GA: for ensemble "+str(ensemble)+" started.")
    killcount = 0 
    
    newcomer_list = []
    for element in ensemble:
        try:
            element.score = ensemble.scorer(element)
            logging.info("GA: Scoring Network "+str(element))
        except: 
            logging.error("GA: The scoring of the element failed.")
        
        if ensemble.selector(element,**kwargs):
            
            newcomer = element.copy()
            logging.info("GA: Mutating Wildtype "+str(element))
            ensemble.mutator(newcomer)
            
            newcomer_list.append(newcomer)
            killcount += 1
            
    
    logging.info("GA: Adding Newcomers")
    for individual in newcomer_list:
        ensemble.add(individual)
        logging.info("New network added, "+str(individual)+".")
        individual.populate_equilibria()
        individual.score = ensemble.scorer(individual)
    
    logging.info("GA: Killing...")
    ensemble.killer(ensemble,killcount)


