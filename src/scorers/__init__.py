def sum_scorer(network):
    # The worst case is an orbit that walks the whole state space.
    # Thus the scores are normalized to that value.
    return sum(network.equilibria)/(2.0**(2*network.n_nodes))