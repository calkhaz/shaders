from gaussian import linear_sampled_kernel
d = dict

sigma = 30.0
intensity = 0.25

# Get weights and offsets from sigma
gaussian_weights, gaussian_offsets = linear_sampled_kernel(sigma)

usm1 = d(
    weights = gaussian_weights.tolist(),
    offsets = gaussian_offsets.tolist(),
    radius = len(gaussian_weights)
)

usm2 = usm1.copy()
usm2['intensity'] = intensity


nodes = d(
    unsharp_mask_pass_1 = usm1,
    unsharp_mask_pass_2 = usm2,
)

#'''
graph = '''
input -> unsharp_mask_pass_1 -> unsharp_mask_pass_2 -> output
input -> unsharp_mask_pass_2:source_image
'''
