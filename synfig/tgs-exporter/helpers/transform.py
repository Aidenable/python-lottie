"""
This module will store all the functions required for transformations
corresponding to lottie
"""

import sys
import settings
from misc import Count
from properties.value import gen_properties_value
from properties.valueKeyframed import gen_value_Keyframed
from properties.multiDimensionalKeyframed import gen_properties_multi_dimensional_keyframed
sys.path.append("../")


def gen_helpers_transform(lottie, layer, pos=[0, 0], anchor=[0, 0, 0], scale=[100, 100, 100]):
    """
    Generates the dictionary corresponding to helpers/transform.json

    Args:
        lottie (dict)                : Lottie format layer
        layer  (lxml.etree._Element) : Synfig format layer
        pos    (:obj: `list | lxml.etree._Element`, optional) : position of layer
        anchor (:obj: `list`) : anchor point of layer
        scale (:obj: `list | lxml.etree._Element`, optional) : scale of layer

    Returns:
        (None)
    """
    index = Count()
    lottie["o"] = {}    # opacity/Amount
    lottie["r"] = {}    # Rotation of the layer
    lottie["p"] = {}    # Position of the layer
    lottie["a"] = {}    # Anchor point of the layer
    lottie["s"] = {}    # Scale of the layer

    # setting the default location
    if isinstance(pos, list):
        gen_properties_value(lottie["p"],
                             pos,
                             index.inc(),
                             settings.DEFAULT_ANIMATED,
                             settings.NO_INFO)
    else:
        gen_properties_multi_dimensional_keyframed(lottie["p"],
                                                   pos,
                                                   index.inc())

    # setting the default opacity i.e. 100
    gen_properties_value(lottie["o"],
                         settings.DEFAULT_OPACITY,
                         index.inc(),
                         settings.DEFAULT_ANIMATED,
                         settings.NO_INFO)

    # setting the rotation
    gen_properties_value(lottie["r"],
                         settings.DEFAULT_ROTATION,
                         index.inc(),
                         settings.DEFAULT_ANIMATED,
                         settings.NO_INFO)

    # setting the anchor point
    gen_properties_value(lottie["a"],
                         anchor,
                         index.inc(),
                         settings.DEFAULT_ANIMATED,
                         settings.NO_INFO)

    # setting the scale
    if isinstance(scale, list):
        gen_properties_value(lottie["s"],
                             scale,
                             index.inc(),
                             settings.DEFAULT_ANIMATED,
                             settings.NO_INFO)
    # This means scale parameter is animated
    else:
        gen_value_Keyframed(lottie["s"], scale, index.inc())
