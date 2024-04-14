import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime


# # potential_field = Vector(-2, -2, -2), Vector(2, 2, 2), {"x": 666, "y": 666}, (0, 0, 0))
# loop_speed = []
# vectorise_speed = []
# meshgrid_speed = []
# total_speed = []
# list_i = []
# for i in range(1, 75):
#     list_i.append(i)
#     x_positions, y_positions, z_positions = np.linspace(-2,2,666), np.linspace(-2,2,i), np.linspace(-2,2,666)

#     start = time.time()
#     array = np.zeros((len(x_positions), len(y_positions), len(z_positions)))
#     for i_x, x in enumerate(x_positions):
#         for i_y, y in enumerate(y_positions):
#             for i_z, z in enumerate(z_positions):
#                 array[i_x, i_y, i_z] = x * y * z
#     # print(array)
#     loop_end = time.time()
#     loop_speed.append(loop_end-start)
#     # print(f"Loop done in {loop_end-start} seconds")

#     vectorized_multiply = np.vectorize(lambda x, y, z: x * y * z)

#     X, Y, Z = np.meshgrid(x_positions, y_positions, z_positions)
#     meshgrid_end = time.time()
#     meshgrid_speed.append(meshgrid_end-loop_end)
#     array_2 = vectorized_multiply(X, Y, Z).swapaxes(0,1)
#     # print(array_2)
#     vectorise_end = time.time()
#     vectorise_speed.append(vectorise_end - meshgrid_end)
#     total_speed.append(vectorise_end-loop_end)
#     # print(f"np.vectorize done in {time_3-time_2} seconds")

#     print(np.array_equal(array, array_2))

# plt.plot(list_i, loop_speed, label="loop")
# plt.plot(list_i, vectorise_speed, label="vectorise")
# plt.plot(list_i, meshgrid_speed, label="meshgrid")
# plt.plot(list_i, total_speed, label="total")
# plt.legend()
# plt.show()


# s = datetime.now()
# print(datetime.now())

# time.sleep(2)

# t = datetime.now()

# print((t-s))
# print((datetime.timedelta(t-s)))

# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# a = np.array([
#     [1,2,3],
#     [4,5,6]
# ])

# print(a.transpose())

# a = [1,2,3]
# b = [4,5,6]

# print(a+b)

# a = "barbi.ecsv"
# print(a.endswith(".csv"))

# if {1}:
#     print("allo")

# print(".".join(["a", "b", "c", "d"]))

# e = ["ab", "cd", "ef"]
# print(e.index("ab"))

# print("allo".split(","))

# print(5<4<7)
# func = eval("lambda x: x > 3")
# print(func(5))

# print([] + ["a"])

# print("\n".join(["1","2","3"]))

print([1,2,3][:])
print(list(reversed([1,2,3])))