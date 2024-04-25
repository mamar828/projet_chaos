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

# print([1,2,3][:])
# print(list(reversed([1,2,3])))


# import matplotlib.pyplot as plt
# import numpy as np

# # set up the figure and axes
# fig = plt.figure(figsize=(7, 7))
# ax1 = fig.add_subplot(projection='3d')

# # fake data
# _x = np.arange(4)
# _y = np.arange(5)
# _xx, _yy = np.meshgrid(_x, _y)
# x, y = _xx.ravel(), _yy.ravel()

# top = x + y
# bottom = np.zeros_like(top)
# width = depth = 1

# ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
# ax1.set_title('Shaded')

# plt.show()

# """
# 2.99421279e+02  4.50000290e+02  0.00000000e+00  0.00000000e+00  -2.90041181e-05  0.00000000e+00  2.91942000e+07
# 2.96377328e+02  4.49995371e+02  0.00000000e+00  3.77473186e-09  -2.95952107e-05  0.00000000e+00  2.37582000e+07
# 6.02108560e+02  4.49999234e+02  0.00000000e+00  1.15437529e-09   2.92882847e-05  0.00000000e+00  1.00000000e+08
# 3.69066864e+02  3.20767901e+02  0.00000000e+00  2.45018463e-05  -1.59090653e-05  0.00000000e+00  3.00000000e+08
# 3.73417840e+02  5.79474457e+02  0.00000000e+00 -2.56404042e-05  -1.48102857e-05  0.00000000e+00  1.00000000e+09
# """
# l = np.array([
#     2.91942000e+07,
#     2.37582000e+07,
#     3.13908200e+08,
#     7.18294200e+08,
#     1.00000000e+09,
#     1.14020000e+06
# ])
# print(np.round(l/(8766*3600), 3))

# # 0.925
# # 0.753
# # 3.169
# # 9.506
# # 31.688


# """
# [[ 2.99421279e+02  4.50000290e+02  0.00000000e+00  0.00000000e+00 -2.90041181e-05  0.00000000e+00  2.91942000e+07]
#  [ 2.96377328e+02  4.49995371e+02  0.00000000e+00  3.77473186e-09 -2.95952107e-05  0.00000000e+00  2.37582000e+07]
#  [ 6.02098562e+02  4.49991236e+02  0.00000000e+00  2.24181434e-09  2.92902520e-05  0.00000000e+00  3.13908200e+08]
#  [ 3.75170843e+02  3.13889252e+02  0.00000000e+00  2.51040864e-05 -1.38416781e-05  0.00000000e+00  7.18294200e+08]
#  [ 3.73417840e+02  5.79474457e+02  0.00000000e+00 -2.56404042e-05 -1.48102857e-05  0.00000000e+00  1.00000000e+09]
#  [ 2.96370352e+02  4.50009903e+02  0.00000000e+00  2.89885694e-08 -2.96187377e-05  0.00000000e+00  1.14020000e+06]]
# """


print(int(False))