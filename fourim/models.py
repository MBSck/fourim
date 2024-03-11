import astropy.units as u
import matplotlib.pyplot as plt
from ppdmod.basic_components import Ring


ring = Ring(rin=2, width=1.5)
image = ring.compute_image(512, 0.1, [10]*u.um)
plt.imshow(image)
plt.show()

