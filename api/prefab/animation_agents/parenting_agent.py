from ...scene.content import Actor, SceneContent


class ParentingActor(Actor):
    def __init__(self, parent: SceneContent, child: SceneContent) -> None:
        super().__init__()
        self.parent = parent
        self.child = child

    def update(self):
        self.child.position = self.parent.position
