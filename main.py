from direct.showbase.ShowBase import ShowBase
import math
import direct
from direct.actor.Actor import Actor


dummy = None
faceJoint = None

class MyApp(ShowBase):
    key_map = {"w": False, "s": False, "a": False, "d": False, "e": False, "q": False,
               "arrow_left": False, "arrow_right": False}


    def __init__(self):
        global dummy
        global faceJoint

        ShowBase.__init__(self)


        # Load the environment model.

        # self.scene = Actor("./model.gltf")
        model = self.loader.load_model("./model.gltf")
        parts = {}
        anims = {}
        p2 = {}
        for np in model.getChildren():
            if np.getName() == "Face":
                p2["modelRoot"] = np
            else:
                parts[np.get_name() if np.get_name() != "Body" else "modelRoot"] = np
                anims[np.get_name] = {}
        print(p2)
        self.face = Actor(models=p2, anims={"modelRoot":{}})
        self.face.listJoints()

        self.scene = Actor(models=parts, anims=anims)
        headJoint = self.scene.exposeJoint(None, "modelRoot", "J_Bip_C_Head")
        self.face.setPos(0, 0, -1.4)
        self.face.reparentTo(headJoint)
        faceJoint = self.face.controlJoint(None, "modelRoot", "29")
        for c in self.scene.getChildren():

            print(c.getName())
            if c.getName() == "Hairs":
                c.reparentTo(headJoint)
                c.setPos(0, 0, -1.4)

        dummy = self.scene.controlJoint(None, "modelRoot", "J_Bip_C_Neck")
        # self.scene.listJoints()

        # Reparent the model to render.

        self.scene.reparentTo(self.render)
        self.disableMouse()

        # Apply scale and position transforms on the model.

        self.scene.setScale(12, 12, 12)
        self.scene.setPos(0, -15, 0)
        self.scene.setH(180)
        self.camera.setY(-40)
        self.taskMgr.add(self.moveCamera, "MoveCamera")
        self.taskMgr.add(self.controlJoint, "ControlJoint")
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

    def controlJoint(self, task):
        global dummy
        global faceJoint

        dummy.setP(math.sin(task.time * 5) * 20)
        faceJoint.setX((math.sin(task.time * 5) + 1) * 0.5)
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

    def moveCamera(self, task):
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

        return direct.task.Task.cont



app = MyApp()

app.run()