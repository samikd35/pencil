"""Planar pose geometry, not a motion generator or physics simulation.

Call with a deliberately posed pole in the same plane as the endpoints.
Calibrate against the drawing's neutral pose before authoring movement.
"""
import math


def two_bone_joint(start, end, lengths, pole):
    """Return the bend joint; reject unreachable or ambiguous input.

    A pole selects the bend side. Do not use a global left/right sign for
    different drawings or views, and do not silently stretch to meet a target.
    """
    if any(len(p) != 2 for p in (start, end, pole)) or len(lengths) != 2:
        raise ValueError('Expected planar points and two segment lengths')
    values = [*start, *end, *pole, *lengths]
    if not all(math.isfinite(v) for v in values) or min(lengths) <= 0:
        raise ValueError('Coordinates must be finite; lengths must be positive')
    dx, dy = end[0]-start[0], end[1]-start[1]
    d = math.hypot(dx, dy)
    a, b = lengths
    if d == 0 or not abs(a-b) <= d <= a+b:
        raise ValueError('Unreachable endpoint; revise the pose or contact plan')
    along = (a*a - b*b + d*d) / (2*d)
    height = math.sqrt(max(0, a*a - along*along))
    cross = dx*(pole[1]-start[1]) - dy*(pole[0]-start[0])
    if height > 1e-9 and abs(cross) < 1e-12:
        raise ValueError('Pole lies on limb axis; choose a bend direction')
    side = 1 if cross >= 0 else -1
    return (start[0] + dx/d*along - dy/d*height*side,
            start[1] + dy/d*along + dx/d*height*side)


if __name__ == '__main__':
    # Both bend directions, exact extension, and invalid targets.
    for bend in [(1, 1), (1, -1)]:
        solved = two_bone_joint((0, 0), (2, 0), (math.sqrt(2), math.sqrt(2)), bend)
        assert math.dist(solved, bend) < 1e-8
    assert two_bone_joint((0, 0), (2, 0), (1, 1), (1, 0)) == (1, 0)
    for end, pole in [((3, 0), (1, 1)), ((0, 0), (1, 1)), ((1, 0), (1, 0)), ((float('nan'), 0), (1, 1))]:
        try:
            two_bone_joint((0, 0), end, (1, 1), pole)
        except ValueError:
            pass
        else:
            raise AssertionError((end, pole))
    print('PASS: bend direction, fixed lengths, extension, invalid/ambiguous targets')
