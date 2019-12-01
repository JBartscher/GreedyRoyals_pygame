from sprite.animated import Animated


def contains(a, b):
    """
    check if a contains b.

    :param a: rectangle a
    :param b: rectangle a
    :return: True if a contains b. Else False.
    """
    if (b.x + b.width < a.x + a.width and
            b.x > a.x and
            b.y > a.y and
            b.y + b.height < a.y + a.height):
        return True
    else:
        return False


def intersects(a: Animated, b: Animated) -> bool:
    """
    check if a intersects with b.

    :param a: rectangle a
    :param b: rectangle b
    :return: True if a intersects b. Else False.
    """
    return (a.x < b.x + b.width and
            a.x + a.width > b.x and
            a.y < b.y + b.height and
            a.y + a.height > b.y)
