"""
    @file:              vector.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create vectors in 3D space.
"""

from typing import NamedTuple


class Vector(NamedTuple):
    """
    Class used to store the x, y and z component of a vectorial quantity, can be used for position, velocity or
    acceleration.

    Elements
    --------
    x : float
        The x component of the vector.
    y : float
        The y component of the vector.
    z : float
        The z component of the vector.
    """

    x: float
    y: float
    z: float
