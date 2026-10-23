from .creature import Creature


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return self.name + " uses Ember!"
