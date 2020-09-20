from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
clueA0 = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, clueA0),
    Implication(AKnave, Not(clueA0))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
clueA1 = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, clueA1),
    Implication(AKnave, Not(clueA1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
clueA2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
clueB2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, clueA2),
    Implication(AKnave, Not(clueA2)),
    Implication(BKnight, clueB2),
    Implication(BKnave, Not(clueB2))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
clueA3 = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
clueB3 = And(Implication(clueA3, BKnave), CKnave)
clueC3 = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Implication(AKnight, clueA3),
    Implication(AKnave, Not(clueA3)),
    Implication(BKnight, clueB3),
    Implication(BKnave, Not(clueB3)),
    Implication(CKnight, clueC3),
    Implication(CKnave, Not(clueC3))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
