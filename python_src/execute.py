import snappy
from . import hikmot
M = snappy.Manifold('4_1(5,1)')
# M = snappy.Manifold('m004(5,1)')
L = hikmot.verify_hyperbolicity(M,0)
print(L[1])
print(M.tetrahedra_shapes('rect'))
