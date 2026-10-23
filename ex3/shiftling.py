from .creature import Creature
from .capability import TransformCapability


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return self.name + " performs a boosted strike!"
        else:
            return self.name + " attacks normally."

    def transform(self) -> str:
        self.transformed = True
        return self.name + " shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return self.name + " returns to normal."
