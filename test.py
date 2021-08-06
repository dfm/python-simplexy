import numpy as np
import matplotlib.pyplot as pl
from simplexy import simplexy

ni, nj = 50, 30
img = np.zeros((ni, nj))
x, y = np.meshgrid(range(ni), range(nj), indexing="ij")

cx, cy = 3.0, 3.0
r2 = (x - cx) ** 2 + (y - cy) ** 2
img += np.exp(-0.5 * r2)

cx, cy = 40.0, 20.0
r2 = (x - cx) ** 2 + (y - cy) ** 2
img += 2*np.exp(-0.25 * r2)

pl.imshow(img, cmap="gray", interpolation="nearest")
pl.savefig("sup.png")

res = simplexy(img)
print(res)
print(res["flux"])
