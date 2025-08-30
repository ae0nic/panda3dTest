from direct.showbase.ShowBase import ShowBase
import math
import direct
from direct.actor.Actor import Actor
from panda3d.core import Shader, DirectionalLight, LVecBase3, LVecBase4f, PointLight

from direct.gui.OnscreenText import OnscreenText

from VRMLoader import VRMLoader

class MyApp(ShowBase):
    key_map = {"w": False, "s": False, "a": False, "d": False, "e": False, "q": False,
               "arrow_left": False, "arrow_right": False, "arrow_down": False, "arrow_up": False}


    def __init__(self):
        ShowBase.__init__(self)

        self.x_text = None
        self.y_text = None
        self.z_text = None

        self.setBackgroundColor(0., 1., 0.)

        # Load the environment model.

        vrm_model = VRMLoader("./model.gltf", self)
        self.scene = vrm_model.body
        self.face = vrm_model.face

        shader = Shader.load(Shader.SL_GLSL,
                             vertex="vert.vert",
                             fragment="frag.frag")
        self.scene.setShader(shader)
        self.scene.setShaderInput("LIGHTS", 2)

        d_light_node = DirectionalLight("d_light")
        d_light_node.setColor((1, 1, 0.8, 1))
        d_light = self.render.attachNewNode(d_light_node)
        d_light.setHpr(40, -45, 0)
        self.scene.setLight(d_light)

        p_light_node = PointLight("p_light")
        p_light_node.setColor((1.5, 1.5, 1.8, 1))
        p_light = self.render.attachNewNode(p_light_node)
        p_light.setPos(0, -40, 15)
        self.scene.setLight(p_light)


        vrm_model.reparent(self.render)
        self.disableMouse()
        self.mouth_target = None


        # Apply scale and position transforms on the model.


        self.scene.setScale(12, 12, 12)
        self.scene.setPos(0, -15, 0)
        self.scene.setH(180)
        self.camera.setY(-40)
        self.taskMgr.add(self.moveCamera, "MoveCamera")
        self.taskMgr.add(self.controlJoint, "ControlJoint", extraArgs=[vrm_model], appendTask=True)
        self.accept("w", self.wDown)
        self.accept("s", self.sDown)
        self.accept("w-up", self.wUp)
        self.accept("s-up", self.sUp)
        self.accept("a", self.aDown)
        self.accept("d", self.dDown)
        self.accept("a-up", self.aUp)
        self.accept("d-up", self.dUp)
        self.accept("e", self.eDown)
        self.accept("q", self.qDown)
        self.accept("e-up", self.eUp)
        self.accept("q-up", self.qUp)
        self.accept("arrow_left", self.arrow_leftDown)
        self.accept("arrow_right", self.arrow_rightDown)
        self.accept("arrow_left-up", self.arrow_leftUp)
        self.accept("arrow_right-up", self.arrow_rightUp)
        self.accept("arrow_down", self.arrow_downDown)
        self.accept("arrow_up", self.arrow_upDown)
        self.accept("arrow_down-up", self.arrow_downUp)
        self.accept("arrow_up-up", self.arrow_upUp)
        self.face_joint = None

    def controlJoint(self, model: VRMLoader, task):
        model.get_morph_target("29").setX((math.sin(task.time * 5) + 1) * 0.5)
        return direct.task.Task.cont

    def wDown(self):
        self.key_map["w"] = True

    def wUp(self):
        self.key_map["w"] = False

    def sDown(self):
        self.key_map["s"] = True

    def sUp(self):
        self.key_map["s"] = False

    def aDown(self):
        self.key_map["a"] = True

    def aUp(self):
        self.key_map["a"] = False

    def dDown(self):
        self.key_map["d"] = True

    def dUp(self):
        self.key_map["d"] = False

    def eDown(self):
        self.key_map["e"] = True

    def eUp(self):
        self.key_map["e"] = False

    def qDown(self):
        self.key_map["q"] = True

    def qUp(self):
        self.key_map["q"] = False

    def arrow_leftDown(self):
        self.key_map["arrow_left"] = True

    def arrow_leftUp(self):
        self.key_map["arrow_left"] = False

    def arrow_rightDown(self):
        self.key_map["arrow_right"] = True

    def arrow_rightUp(self):
        self.key_map["arrow_right"] = False

    def arrow_upDown(self):
        self.key_map["arrow_up"] = True

    def arrow_upUp(self):
        self.key_map["arrow_up"] = False

    def arrow_downDown(self):
        self.key_map["arrow_down"] = True

    def arrow_downUp(self):
        self.key_map["arrow_down"] = False

    def moveCamera(self, task):
        if self.x_text is None:
            self.x_text = OnscreenText(text="X: " + str(self.camera.getX()), pos=(-1, 0.9), scale=0.07)
            self.y_text = OnscreenText(text="Y: " + str(self.camera.getY()), pos=(-1, 0.8), scale=0.07)
            self.z_text = OnscreenText(text="Z: " + str(self.camera.getZ()), pos=(-1, 0.7), scale=0.07)

        self.x_text.setText("X: " + str(self.camera.getX()))
        self.y_text.setText("Y: " + str(self.camera.getY()))
        self.z_text.setText("Z: " + str(self.camera.getZ()))

        if self.key_map["w"]:
            self.camera.setY(self.camera.getY() + 1)

        if self.key_map["s"]:
            self.camera.setY(self.camera.getY() - 1)

        if self.key_map["a"]:
            self.camera.setX(self.camera.getX() - 1)

        if self.key_map["d"]:
            self.camera.setX(self.camera.getX() + 1)

        if self.key_map["e"]:
            self.camera.setZ(self.camera.getZ() + 1)

        if self.key_map["q"]:
            self.camera.setZ(self.camera.getZ() - 1)

        if self.key_map["arrow_left"]:
            self.camera.setH(self.camera.getH() + 1)

        if self.key_map["arrow_right"]:
            self.camera.setH(self.camera.getH() - 1)

        if self.key_map["arrow_down"]:
            self.camera.setP(self.camera.getP() - 1)

        if self.key_map["arrow_up"]:
            self.camera.setP(self.camera.getP() + 1)

        return direct.task.Task.cont



app = MyApp()

app.run()