"""
    @file:              vector.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create vectors in 3D space.
"""
from __future__ import annotations

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

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


class FakeVector:
    """
    Class used to store the x, y and z component of a vectorial quantity but with values that can be changed.
    """

    def __init__(self, x, y, z):
        """
        Sets required parameters

        Parameters
        ----------
        x : float
            The x component of the vector.
        y : float
            The y component of the vector.
        z : float
            The z component of the vector.
        """
        self.x = x
        self.y = y
        self.z = z

    def vectorise(self) -> Vector:
        """
        Returns a Vector object with the same components as the FakeVector Object

        Returns
        -------
        vector : Vector
            The corresponding Vector object.
        """

        return Vector(self.x, self.y, self.z)

    @staticmethod
    def fakevectorise(vector: Vector) -> FakeVector:
        """
        Returns a FakeVector object with the same components as the Vector Object

        Returns
        -------
        fakevector : FakeVector
            The corresponding FakeVector object.
        """

        return FakeVector(vector.x, vector.y, vector.z)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return FakeVector(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return FakeVector(self.x-other.x, self.y-other.y, self.z-other.z)

    def __rmul__(self, other):
        return FakeVector(self.x * other.x, self.y * other.y, self.z * other.z)
