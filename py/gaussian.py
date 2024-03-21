from utils.gaussian_kernel import linear_sampled_kernel
d = dict

# TODO: Fix 0.0 not actually being completely unblurred
sigma = 30.0

# Get weights and offsets from sigma
gaussian_weights, gaussian_offsets = linear_sampled_kernel(sigma)

gaussian = d(
    weights = gaussian_weights.tolist(),
    offsets = gaussian_offsets.tolist(),
    radius = len(gaussian_weights)
)

nodes = d(
    gaussian_v = gaussian,
    gaussian_h = gaussian,
)

graph = 'input ->  gaussian_h -> gaussian_v -> output'
