from utils.gaussian_kernel import linear_sampled_kernel

ui = dict(
    sharpness            = dict(val = 25,  min = 1,    max = 25),
    sigma                = dict(val = 2.0, min = 0.0,  max = 50.0),
    kernel_radius        = dict(val = 9,   min = 2,    max = 30),
    ellipse_eccentricity = dict(val = 5.0, min = 0.1,  max = 20.0),
    usm_intensity        = dict(val = 0.1, min = 0.0,  max = 1.0),
    usm_sigma            = dict(val = 5.0, min = 0.1,  max = 20.0),
    saturation           = dict(val = 1.2, min = 0.0,  max = 2.0),
    contrast             = dict(val = 1.0, min = 0.0,  max = 2.0),
    brightness           = dict(val = 0.0, min = 0.0,  max = 2.0),
    hue                  = dict(val = 0.0, min = 0.0,  max = 6.28318),
)


def build_nodes(ui: dict) -> dict[str, dict[str, float|int]]:
    # Get weights and offsets from sigma
    gaussian_weights, gaussian_offsets = linear_sampled_kernel(ui['sigma'])
    usm_gaussian_weights, usm_gaussian_offsets = linear_sampled_kernel(ui['usm_sigma'])

    usm1 = dict(
        weights = usm_gaussian_weights.tolist(),
        offsets = usm_gaussian_offsets.tolist(),
        radius = len(usm_gaussian_weights)
    )

    usm2 = usm1.copy()
    usm2['intensity'] = ui['usm_intensity']
    
    gaussian = dict(
        weights = gaussian_weights.tolist(),
        offsets = gaussian_offsets.tolist(),
        radius = len(gaussian_weights)
    )
    
    kuwahara_anisotropic = dict(
        sharpness = ui['sharpness'],
        kernel_radius = ui['kernel_radius'],
        ellipse_eccentricity = ui['ellipse_eccentricity']
    )

    color_adjust = dict(
        saturation = ui['saturation'],
        contrast = ui['contrast'],
        brightness = ui['brightness'],
        hue = ui['hue']
    )

    nodes = dict(
        gaussian_v = gaussian,
        gaussian_h = gaussian,
        kuwahara_anisotropic = kuwahara_anisotropic,
        unsharp_mask_pass_1 = usm1,
        unsharp_mask_pass_2 = usm2,
        color_adjust = color_adjust
    )

    return nodes

graph = '''
input -> color_adjust -> kuwahara_anisotropic
         color_adjust -> structure_tensor -> gaussian_h -> gaussian_v -> kuwahara_anisotropic:structure_tensor
                                                                         kuwahara_anisotropic -> unsharp_mask_pass_2:source_image
                                                                         kuwahara_anisotropic -> unsharp_mask_pass_1 -> unsharp_mask_pass_2 -> output
'''
