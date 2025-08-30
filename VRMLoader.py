from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath


class VRMLoader():

    def __init__(self, file: str, app: ShowBase):
        self.joints = {}

        model = app.loader.loadModel(file)

        body_parts = {}
        body_animations = {}
        face_parts = {}
        face_animations = {}

        for np in model.get_children():
            if np.get_name() == "Face":
                face_parts["modelRoot"] = np
                face_animations["modelRoot"] = {}
            else:
                body_parts[np.get_name() if np.get_name() != "Body" else "modelRoot"] = np
                body_animations[np.get_name() if np.get_name() != "Body" else "modelRoot"] = {}



        self.body = Actor(models=body_parts, anims=body_animations)
        self.face = Actor(models=face_parts, anims=face_animations)
        # self.face.listJoints()
        self.face.setPos(0, 0, -1.4)

        head_joint = self.body.exposeJoint(None, "modelRoot", "J_Bip_C_Head")

        self.face.reparentTo(head_joint)

        for c in self.body.getChildren():
            if c.getName() == "Hairs":
                c.setPos(0, 0, -1.4)
                c.reparentTo(head_joint)

    def reparent(self, path: NodePath):
        self.body.reparentTo(path)

    def get_morph_target(self, name: str):
        """
        Returns the result of controlJoint() called on the face.
        :param name: The name of the morph target to obtain, which is probably a number.
        :return: A NodePath representing the morph target. Using setX() moves the morph target.
        """
        if self.joints.get(name) is None:
            self.joints[name] = self.face.controlJoint(None, "modelRoot", name)
        return self.joints.get(name)

    def get_joint(self, name: str) -> NodePath:
        """
        Returns the result of controlJoint() called on the body.
        :param name: The name of the joint to obtain.
        :return: A NodePath representing the joint.
        """
        if self.joints.get(name) is None:
            self.joints[name] = self.body.controlJoint(None, "modelRoot", name)
        return self.joints.get(name)