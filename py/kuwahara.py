from utils.gaussian_kernel import linear_sampled_kernel

sharpness = 25
sigma = 2.0
kernel_radius = 9
ellipse_eccentricity = 1.9

def build_nodes() -> dict[str, dict[str, float|int]]:
    # Get weights and offsets from sigma
    gaussian_weights, gaussian_offsets = linear_sampled_kernel(sigma)
    
    gaussian = dict(
        weights = gaussian_weights.tolist(),
        offsets = gaussian_offsets.tolist(),
        radius = len(gaussian_weights)
    )
    
    kuwahara_anisotropic = dict(
        sharpness = sharpness,
        kernel_radius = kernel_radius,
        ellipse_eccentricity = ellipse_eccentricity
    )

    nodes = dict(
        gaussian_v = gaussian,
        gaussian_h = gaussian,
        kuwahara_anisotropic = kuwahara_anisotropic,
    )

    return nodes

nodes = build_nodes()

graph = '''
input -> structure_tensor -> gaussian_h -> gaussian_v -> kuwahara_anisotropic:structure_tensor
                                                input -> kuwahara_anisotropic -> output
'''
