from .creature import Creature
from .capability import TransformCapability


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return self.name + " unleashes a devastating morph strike!"
        else:
            return self.name + " attacks normally."

    def transform(self) -> str:
        self.transformed = True
        return self.name + " morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.transformed = False
        return self.name + " stabilizes its form."
