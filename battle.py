from ex3 import FlameFactory
from ex3 import TransformCreatureFactory
from ex3 import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    print("Testing battle")
    fighter1 = factory1.create_base()
    fighter2 = factory2.create_base()
    print(fighter1.describe())
    print("vs.")
    print(fighter2.describe())
    print("fight!")
    print(fighter1.attack())
    print(fighter2.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    test_factory(flame)
    test_factory(transform)
    test_battle(flame, transform)
