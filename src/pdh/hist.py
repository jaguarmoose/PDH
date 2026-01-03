import matplotlib.pyplot as plt
from numpy.random import normal, uniform
gaussian_numbers = normal(size=1000)
uniform_numbers = uniform(low=-3, high=3, size=1000)
plt.hist(gaussian_numbers, bins=20, histtype='stepfilled', normed=True, color='b', label='Gaussian')
plt.hist(uniform_numbers, bins=20, histtype='stepfilled', normed=True, color='r', alpha=0.5, label='Uniform')
plt.title("Gaussian/Uniform Histogram")
plt.xlabel("Value")
plt.ylabel("Probability")
plt.legend()
plt.show()
