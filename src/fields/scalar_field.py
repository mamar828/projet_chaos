"""
    @file:              scalar_field.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create the basic structure of a scalar field.
"""

from typing import Dict, List, Tuple

from numpy import sqrt, linspace, zeros, ndarray

from src.tools.vector import Vector
from src.fields.base_field import Field


class ScalarField(Field):
    """
    A class used to compute and define a scalar field.
    """

    def __init__(self, terms: List[Tuple[float, float, Vector]]):
        """
        Defines the required parameters.

        Parameters
        ----------
        terms : List[Tuple[float, float, Vector]]
            A list of the different terms of the equation defining the field. Each term is composed of a tuple with
            three elements: the position's power within the term, the coefficient multiplying the position factor and
            the origin from which the term is computed.
        """

        self.terms = terms

    def __add__(self, other):
        """
        Adds two fields together.

        Returns
        -------
        updated_field : ScalarField
            The field made from the sum of the two fields.
        """

        updated_terms = self.terms
        updated_terms += other.terms
        return ScalarField(updated_terms)

    def __sub__(self, other):
        """
        Subtracts the second field from the first.

        Returns
        -------
        updated_field : ScalarField
            The field made from the difference of the two fields.
        """

        updated_terms = self.terms
        for term in other.terms:
            if term in updated_terms:
                updated_terms.remove(term)
            else:
                updated_terms.append((term[0], -term[1], term[2]))
        return ScalarField(updated_terms)

    def __mul__(self, other):
        """
        Multiplies the field by a scalar value.

        Returns
        -------
        updated_field : ScalarField
            The field made from the scalar product of the field with the scalar value.
        """

        if not isinstance(other, float) and not isinstance(other, int):
            raise NotImplementedError(f"Only scalar multiplication of a scalar field is implemented. The given object "
                                      f"was of type {type(other)}")
        updated_terms = []
        for term in self.terms:
            updated_terms.append((term[0], other*term[1], term[2]))
        return ScalarField(updated_terms)

    def __rmul__(self, other):
        """
        Multiplies the field by a scalar value.

        Returns
        -------
        updated_field : ScalarField
            The field made from the scalar product of the field with the scalar value.
        """

        return self * other

    def __call__(self, position: Vector) -> float:
        """
        Computes the value of the scalar field at a desired position.

        Parameters
        ----------
        position : Vector
            The Vector object representing the position of the point where the field should be evaluated.

        Returns
        -------
        value : float
            The value of the field at the given position.
        """
        value = 0
        for term in self.terms:
            relative_distance = sqrt((term[2].x-position.x)**2+(term[2].y-position.y)**2+(term[2].z-position.z)**2)
            value += term[1]*(relative_distance**term[0])

        return value

    def get_gradient(self, position: Vector, epsilon: float = 10**(-2)) -> Vector:
        """
        Computes the gradient of the scalar field at a given position using a step of size epsilon.

        Parameters
        ----------
        position : Vector
            The position where the gradient should be evaluated
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).

        Returns
        -------
        gradient : Vector
            The gradient at the desired position.
        """

        x, y, z = position
        return Vector(
            (self(Vector(x + epsilon/2, y, z)) - self(Vector(x - epsilon/2, y, z)))/epsilon,
            (self(Vector(x, y + epsilon/2, z)) - self(Vector(x, y - epsilon/2, z)))/epsilon,
            (self(Vector(x, y, z + epsilon/2)) - self(Vector(x, y, z - epsilon/2)))/epsilon,
        )

    def get_acceleration(self, position: Vector, epsilon: float = 10**(-2)) -> Vector:
        """
        Computes the gradient of the scalar field at a given position using a step of size epsilon.

        Parameters
        ----------
        position : Vector
            The position where the gradient should be evaluated
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).

        Returns
        -------
        gradient : Vector
            The gradient at the desired position.
        """

        x, y, z = position
        return Vector(
            -(self(Vector(x + epsilon/2, y, z)) - self(Vector(x - epsilon/2, y, z)))/epsilon,
            -(self(Vector(x, y + epsilon/2, z)) - self(Vector(x, y - epsilon/2, z)))/epsilon,
            -(self(Vector(x, y, z + epsilon/2)) - self(Vector(x, y, z - epsilon/2)))/epsilon,
        )

    def _compute_field_wide_operations(
            self,
            start: Vector,
            stop: Vector,
            function,
            nb_ticks_per_axis: Dict[str, int] = None,
            origin_position: Tuple[float, float, float] = None
    ):
        """
        Computes the value of a certain function on a grid and returns its values as a numpy array.

        Parameters
        ----------
        start : Vector
            The position of the starting corner of the space cube.
        stop : Vector
            The position of the stopping corner of the space cube.
        function
            Callable object that defines the operation to apply on all array elements. This function must take as
            argument a Vector object of the three axis positions such as function(Vector(x, y, z)).
        nb_ticks_per_axis : Dict[str, int]
            The number of steps between the starting and stopping positions for each axis in the form of {axis, value}.
            Defaults to 100 values per dimension.
        origin_position : Tuple[float, float, float]
            The position of the origin within the given space cube. It is of no consequence for 3D arrays, but for
            arrays with fewer dimensions it determines the position of the plane for the missing dimensions. Defaults to
            (0, 0, 0).

        Returns
        -------
        array : ndarray
            The array of the computed function at the specified coordinates.
        """

        if not callable(function):
            raise TypeError("The function must be callable")
        if nb_ticks_per_axis is None:
            nb_ticks_per_axis = {"x": 100, "y": 100, "z": 100}
        if origin_position is None:
            origin_position = [0], [0], [0]
        x_positions, y_positions, z_positions = [origin_position[0]], [origin_position[1]], [origin_position[2]]
        for axis, nb_ticks in nb_ticks_per_axis.items():
            if axis == "x":
                x_positions = linspace(getattr(start, axis), getattr(stop, axis), int(nb_ticks))
            if axis == "y":
                y_positions = linspace(getattr(start, axis), getattr(stop, axis), int(nb_ticks))
            if axis == "z":
                z_positions = linspace(getattr(start, axis), getattr(stop, axis), int(nb_ticks))
        array = zeros((len(x_positions), len(y_positions), len(z_positions)))
        for i_x, x in enumerate(x_positions):
            for i_y, y in enumerate(y_positions):
                for i_z, z in enumerate(z_positions):
                    array[i_x, i_y, i_z] = function(Vector(x, y, z))

        return array

    def get_potential_field(
            self,
            start: Vector,
            stop: Vector,
            nb_ticks_per_axis: Dict[str, int] = None,
            origin_position: Tuple[float, float, float] = None,
    ) -> ndarray:
        """
        Computes the value of the field a grid and returns the result as a numpy array.

        Parameters
        ----------
        start : Vector
            The position of the starting corner of the space cube.
        stop : Vector
            The position of the stopping corner of the space cube.
        nb_ticks_per_axis : Dict[str, int]
            The number of steps between the starting and stopping positions for each axis in the form of {axis, value}.
            Defaults to 100 values per dimension.
        origin_position : Tuple[float, float, float]
            The position of the origin within the given space cube. It is of no consequence for 3D arrays, but for
            arrays with fewer dimensions it determines the position of the plane for the missing dimensions. Defaults to
            (0, 0, 0).

        Returns
        -------
        array : ndarray
            The array of the field's values at the specified coordinates.
        """

        return self._compute_field_wide_operations(
            start,
            stop,
            lambda vector: self(vector),
            nb_ticks_per_axis,
            origin_position
        )

    def get_gradient_field(
            self,
            start: Vector,
            stop: Vector,
            nb_ticks_per_axis: Dict[str, int] = None,
            origin_position: Tuple[float, float, float] = None
    ) -> ndarray:
        """
        Computes the gradient of the field a grid and returns the result as a numpy array.

        Parameters
        ----------
        start : Vector
            The position of the starting corner of the space cube.
        stop : Vector
            The position of the stopping corner of the space cube.
        nb_ticks_per_axis : Dict[str, int]
            The number of steps between the starting and stopping positions for each axis in the form of {axis, value}.
            Defaults to 100 values per dimension.
        origin_position : Tuple[float, float, float]
            The position of the origin within the given space cube. It is of no consequence for 3D arrays, but for
            arrays with fewer dimensions it determines the position of the plane for the missing dimensions. Defaults to
            (0, 0, 0).

        Returns
        -------
        array : ndarray
            The array of the field's gradient at the specified coordinates.
        """

        return self._compute_field_wide_operations(
            start,
            stop,
            lambda vector: self.get_gradient(vector),
            nb_ticks_per_axis,
            origin_position,
        )


