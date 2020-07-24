# This is a python script to verify all manifolds in the cusped census. To show that a manifold is
# hyperbolic we only need to show that one triangulation of a given manifold is provably hyperbolic 
# by our method. In fact, we show that either the given triangulation of snappy is provably hyperbolic
# or the canonical triangulation is. Although with enough precision, one should be able to verify
# that all triangulations in the census are hyperbolic, checking either one is sufficient for our
# purposes.

import hikmot
import snappy


Census = snappy.OrientableCuspedCensus()
print_data = 0
save_data = 0

num_goods = 0
BadList = []
num_bads = 0
old_num_bads = 0

print("Iterating over {0} manifolds...".format(len(snappy.OrientableCuspedCensus())))

i = 0
for M in snappy.OrientableCuspedCensus():
    i = i+1
    N = M.copy()
    error_data = None

    known_canonized = False
    while not known_canonized:
        try:
            N.canonize()
            known_canonized = True
        except snappy.exceptions.SnapPeaFatalError:
            N.randomize()
            continue
    
    if (hikmot.verify_hyperbolicity(N,print_data, save_data)[0] or hikmot.verify_hyperbolicity(M,print_data, save_data)): # and M.is_isometric_to(N):
        # GoodList.append(N)
        num_goods+=1
    else:
        error_data = (M.name(), M.is_isometric_to(N), hikmot.verify_hyperbolicity(M,print_data, save_data)[0])
        BadList.append((N,error_data))
    if i % 1000 == 0:
        if old_num_bads != num_bads:
            print("XX: {0}, {1}".format(i, BadList[old_num_bads:]))
            old_num_bads = num_bads
        else:
            print("ok: {0}".format(i))
print('Out of {0} manifolds in the OrientableCuspedCensus, {1} have been proven to be hyperbolic and {2} have not.'.format(len(snappy.OrientableCuspedCensus), num_goods, len(BadList)))
