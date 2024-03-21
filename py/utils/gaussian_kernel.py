# https://www.rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/

import numpy as np
from numpy.typing import NDArray
from typing import Tuple

# Set max sigma to at least fit in float[256] offsets & weights
MAX_SIGMA = 130.0

def sigma_to_separable_radius(sigma: float) -> int:
    sigma = MAX_SIGMA if sigma > MAX_SIGMA else sigma

    # *3 is a general allows us to capture most the gaussian's distribution
    kernel_radius = int(sigma*3.0)

    # Set kernel size to odd because each index needs a pair except the center
    kernel_radius += int(not (kernel_radius%2))

    return kernel_radius

def sigma_to_linear_sampled_radius(sigma: float) -> int:
    separable_radius = sigma_to_separable_radius(sigma)

    # Size is odd, so we do -1 to remove the center +1 to add the center
    return int((separable_radius-1)/2+1)

# Create one dimensional separable gaussian kernel
def separable_kernel(sigma: float) -> NDArray[np.float64]:
    if sigma == 0:
        return np.empty(0)

    separable_radius = sigma_to_separable_radius(sigma)
    idx = np.arange(0, separable_radius)

    gauss_constant = 1/(sigma*np.sqrt(2*np.pi))
    sigma_sqr = sigma*sigma

    kernel = gauss_constant * np.exp((-0.5*idx*idx)/sigma_sqr)

    return kernel

def linear_sampled_kernel(sigma: float) -> Tuple[NDArray[np.float64], NDArray[np.float64]]:
    kernel_1d = separable_kernel(sigma)
    linear_radius = sigma_to_linear_sampled_radius(sigma)

    if kernel_1d.size == 0:
        return (np.empty(0), np.empty(0))
    
    idx = np.arange(0, linear_radius)

    weights0 = kernel_1d[2*idx-1]
    weights1 = kernel_1d[2*idx]

    weights = weights0 + weights1
    offsets = ((2*idx-1)*weights0 + (2*idx)*weights1)/weights

    offsets[0] = 0
    weights[0] = kernel_1d[0] 

    # Normalize gaussian weights (Make it so we sum up to 1.0)
    # Reweighting is required if the gaussian is clamped
    #
    # This is a radius, so we do 2* samples for all but the center index 0
    total_weight = weights[0] + float(np.sum(2*weights[1:]))
    weights /= total_weight

    return (weights, offsets)

if __name__ == "__main__":
    weights, offsets = linear_sampled_kernel(25)
    print("num weights/offsets:", len(weights))
    print("weights:", weights)
    print("offsets:", offsets)
    print("total weight: ", print(weights[0]+2*np.sum(weights[1:])))
