from api.sax_engine.core.entities import ActorEntity, ContentEntity

__all__ = ['ParentingAgent']


class ParentingAgent(ActorEntity):
    def __init__(self, parent: ContentEntity, child: ContentEntity) -> None:
        super().__init__()
        self.parent = parent
        self.child = child

    def update(self):
        self.child.position = self.parent.position
