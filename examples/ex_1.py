from kreveik import *

if __name__ == __main__:
	networklet = generate_random(6,scorers.sum_scorer,boolfuncs.xor_masking)
	networklet.print_id()
	
	