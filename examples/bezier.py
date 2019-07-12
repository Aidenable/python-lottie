import sys
import os
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from tgs import exporters
from tgs import objects


an = objects.Animation(59)

layer = objects.ShapeLayer()
an.add_layer(layer)

heart = objects.Bezier()
heart.add_point([50, 20], [50, -20], [-50, -20])
heart.add_smooth_point([0, 50], [-5, -10])
heart.add_smooth_point([50, 100], [-10, 0])
heart.add_smooth_point([100, 50], [-5, 10])
heart.closed = True
antiheart = (
    objects.Bezier()
    .add_smooth_point([50, 0], [10, 0])
    .add_smooth_point([0, 50], [0, -20])
    .add_point([50, 80], [-50, 20], [50, 20])
    .add_smooth_point([100, 50], [0, 20])
    .close()
)

g1 = layer.add_shape(objects.Group())
g1.transform.position.value = [100, 200]
shape = g1.add_shape(objects.Shape())
shape.vertices.value = heart

g2 = layer.add_shape(objects.Group())
g2.transform.position.value = [300, 200]
animated = g2.add_shape(objects.Shape())
animated.vertices.add_keyframe(0, heart)
animated.vertices.add_keyframe(30, antiheart)
animated.vertices.add_keyframe(59, heart)


fill = layer.add_shape(objects.Fill([1, 0, 0]))
stroke = layer.add_shape(objects.Stroke([0, 0, 0], 5))


exporters.multiexport(an, "/tmp/bezier")
