import pykokkos as pk
import numpy as np

pk.initialize()
x = pk.View([10, 4], pk.double)
x[:] = np.asarray([[i, i+100, i+200, i+300] for i in range(10)])

y = pk.View([1], pk.double)
y[0] = 1


print(np.asarray(x)[:, 2])
print(pk.col(x, 2))

# print(1 - np.asarray(x))

# print(x.data)
# print(y.data)
# print(pk.hstack(x, y))
# print(np.hstack((x, y)))
# pk.finalize()