def distance(entity1, entity2):
    return abs(entity1.x - entity2.x) + abs(entity1.y - entity2.y)


def normalize(a: float):
    return 1 if a > 0 else (-1 if a < 0 else 0)
