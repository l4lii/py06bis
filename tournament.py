from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import BattleStrategy, NormalStrategy
from ex4 import AggressiveStrategy, InvalidStrategyError


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                factory1, strategy1 = opponents[i]
                factory2, strategy2 = opponents[j]
                fighter1 = factory1.create_base()
                fighter2 = factory2.create_base()
                print("* Battle *")
                print(f"{fighter1.describe()}")
                print("vs.")
                print(f"{fighter2.describe()}")
                print("now fight!")
                strategy1.act(fighter1)
                strategy2.act(fighter2)
    except InvalidStrategyError as e:
        print("Battle error, aborting tournament:", e)


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    opponents0: list[tuple[CreatureFactory, BattleStrategy]] = [
        (FlameFactory(), NormalStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    print("[ (Flameling+Normal), (Shiftling+Aggressive) ]")
    battle(opponents0)
    print("Tournament 1 (error)")
    opponents1: list[tuple[CreatureFactory, BattleStrategy]] = [
        (TransformCreatureFactory(), AggressiveStrategy()),
        (FlameFactory(), AggressiveStrategy())
    ]
    print("[ (Shiftling+Aggressive), (Flameling+Aggressive) ]")
    battle(opponents1)
