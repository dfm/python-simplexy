import numpy as np
import matplotlib.pyplot as pl
from simplexy import simplexy

cx, cy = 3.0, 3.0
x, y = np.meshgrid(range(50), range(10), indexing="ij")
r2 = (x - cx) ** 2 + (y - cy) ** 2
img = np.exp(-0.5 * r2)

pl.imshow(img, cmap="gray", interpolation="nearest")
pl.savefig("sup.png")

print(simplexy(img)["flux"])
