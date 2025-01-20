from gaussian import linear_sampled_kernel
d = dict

from utils.gaussian_kernel import linear_sampled_kernel

ui = dict(
    usm_intensity = dict(val = 0.2, min = 0.0,  max = 1.0),
    usm_sigma     = dict(val = 40.0, min = 0.1,  max = 50.0)
)


def build_nodes(ui: dict) -> dict[str, dict[str, float|int]]:
    # Get weights and offsets from sigma
    usm_gaussian_weights, usm_gaussian_offsets = linear_sampled_kernel(ui['usm_sigma'])

    usm1 = dict(
        weights = usm_gaussian_weights.tolist(),
        offsets = usm_gaussian_offsets.tolist(),
        radius = len(usm_gaussian_weights)
    )

    usm2 = usm1.copy()
    usm2['intensity'] = ui['usm_intensity']
    
    nodes = dict(
        unsharp_mask_pass_1 = usm1,
        unsharp_mask_pass_2 = usm2,
    )

    return nodes

graph = '''
input -> unsharp_mask_pass_2:source_image
input -> unsharp_mask_pass_1 -> unsharp_mask_pass_2 -> output
'''
