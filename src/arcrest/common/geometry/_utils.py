"""
collection geometry operations
"""
import math


def _myDet(p, q, r):
    """Calc. determinant of a special matrix with three 2D points.

    The sign, "-" or "+", determines the side, right or left,
    respectivly, on which the point r lies, when measured against
    a directed vector from p to q.
    """
    sum1 = q[0]*r[1] + p[0]*q[1] + r[0]*p[1]
    sum2 = q[0]*p[1] + r[0]*q[1] + p[0]*r[1]
    return sum1 - sum2
#--------------------------------------------------------------------------
def _isRightTurn((p, q, r)):
    assert p != q and q != r and p != r
    if _myDet(p, q, r) < 0:
        return 1
    else:
        return 0
#--------------------------------------------------------------------------
def _isPointInPolygon(r, poly):
    """determines if a point is in a polygon

    Output:
      0 - outside
      1 - inside
    """
    for i in xrange(len(poly[:-1])):
        p, q = poly[i], poly[i+1]
        if not _isRightTurn((p, q, r)):
            return 0

    return 1 # It's within!
