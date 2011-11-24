global JOBSERVER

def init():
    import pp
    import sys
    
    ppservers = ()
    #ppservers = ("10.0.0.1",)
    
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        
        JOBSERVER = pp.Server(ncpus, ppservers=ppservers)
        
    else:
        # Creates jobserver with automatically detected number of workers
        
        JOBSERVER = pp.Server(ppservers=ppservers)
    
    print "Starting pp with", JOBSERVER.get_ncpus(), "workers"