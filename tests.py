import numpy as np
import time


# potential_field = Vector(-2, -2, -2), Vector(2, 2, 2), {"x": 666, "y": 666}, (0, 0, 0))

x_positions, y_positions, z_positions = np.linspace(-2,2,666), np.linspace(-2,2,666), np.linspace(-2,2,1)

start = time.time()
array = np.zeros((len(x_positions), len(y_positions), len(z_positions)))
for i_x, x in enumerate(x_positions):
    for i_y, y in enumerate(y_positions):
        for i_z, z in enumerate(z_positions):
            array[i_x, i_y, i_z] = x * y * z
# print(array)
print(f"Loop done in {time.time()-start} seconds")

start_2 = time.time()
vectorized_multiply = np.vectorize(lambda x, y, z: x * y * z)

X, Y, Z = np.meshgrid(x_positions, y_positions, z_positions)

array_2 = vectorized_multiply(X, Y, Z)
# print(array_2)
print(f"np.vectorize done in {time.time()-start_2} seconds")

print(np.array_equal(array, array_2))
