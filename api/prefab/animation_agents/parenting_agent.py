from ...scene.content import Agent, SceneContent


class ParentingAgent(Agent):
    def __init__(self, parent: SceneContent, child: SceneContent) -> None:
        super().__init__()
        self.parent = parent
        self.child = child

    def update_agency(self, delta_time: float):
        self.child.position = self.parent.position
