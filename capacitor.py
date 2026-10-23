from ex3.TransformCreatureFactory import TransformCreatureFactory
from ex3 import TransformCapability
from ex3 import Creature


def test_capability(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if isinstance(creature, TransformCapability):
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


if __name__ == "__main__":
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()
    print("Testing Creature with transform capability")
    print("base:")
    test_capability(base)
    print("evolved:")
    test_capability(evolved)
