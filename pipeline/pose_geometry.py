"""Planar pose geometry, not a motion generator or physics simulation.

Call with a deliberately posed pole in the same plane as the endpoints.
Calibrate against the drawing's neutral pose before authoring movement.
"""
import math


def transported_pole(rest_start, rest_end, rest_pole, start, end):
    """Carry a drawing's bend side with its moving limb axis.

    A fixed world-space pole can cross that axis and abruptly flip the elbow.
    This planar similarity preserves the authored side; deliberate side changes
    need a separate pose/view, not an accidental pole crossing.
    """
    points=(rest_start,rest_end,rest_pole,start,end)
    if any(len(p)!=2 for p in points) or not all(math.isfinite(x) for p in points for x in p):
        raise ValueError('Expected finite planar points')
    rx,ry=rest_end[0]-rest_start[0],rest_end[1]-rest_start[1]
    px,py=rest_pole[0]-rest_start[0],rest_pole[1]-rest_start[1]
    dx,dy=end[0]-start[0],end[1]-start[1];den=rx*rx+ry*ry
    if den<1e-12 or dx*dx+dy*dy<1e-12:raise ValueError('Limb axis must have nonzero length')
    u,v=(px*rx+py*ry)/den,(rx*py-ry*px)/den
    if abs(v)<1e-12:raise ValueError('Rest pole must define a bend side')
    return start[0]+u*dx-v*dy,start[1]+u*dy+v*dx


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
    for degrees in range(-180,181,3):
        t=math.radians(degrees);end=(2*math.cos(t),2*math.sin(t))
        pole=transported_pole((0,0),(2,0),(1,1),(0,0),end)
        joint=two_bone_joint((0,0),end,(math.sqrt(2),math.sqrt(2)),pole)
        assert abs(math.dist((0,0),joint)-math.sqrt(2))<1e-8
        assert end[0]*joint[1]-end[1]*joint[0]>0
    for end, pole in [((3, 0), (1, 1)), ((0, 0), (1, 1)), ((1, 0), (1, 0)), ((float('nan'), 0), (1, 1))]:
        try:
            two_bone_joint((0, 0), end, (1, 1), pole)
        except ValueError:
            pass
        else:
            raise AssertionError((end, pole))
    print('PASS: bend direction, fixed lengths, extension, invalid/ambiguous targets')
