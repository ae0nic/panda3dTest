from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

base = ShowBase()

model = base.loader.loadModel("box")
model.setPos(0, 10, 0)
model.reparentTo(base.render)

d_light_node = DirectionalLight("p_light")
# d_light_node.setDirection((1, 44, 1))
d_light = base.render.attachNewNode(d_light_node)
d_light.setHpr(0, -90, 0)
# d_light_node.setColor(LColor(0.0, 1.0, 0.0, 1.0))

base.render.setLight(d_light)

shader = Shader.load(Shader.SL_GLSL, "example.vert.glsl", "example.frag.glsl")
model.setShader(shader)

base.run()