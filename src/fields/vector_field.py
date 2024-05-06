from typing import List, Tuple
from numpy import sqrt

from src.fields.base_field import Field
from src.tools.vector import FakeVector, Vector


class VectorField(Field):
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
        return VectorField(updated_terms)

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
        return VectorField(updated_terms)

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
        return VectorField(updated_terms)

    def __rmul__(self, other):
        """
        Multiplies the field by a scalar value.

        Returns
        -------
        updated_field : ScalarField
            The field made from the scalar product of the field with the scalar value.
        """

        return self * other

    def __call__(self, position: Vector) -> Vector:
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

        force = FakeVector(0, 0, 0)
        for term in self.terms:
            relative_distance = sqrt((term[2].x-position.x)**2+(term[2].y-position.y)**2+(term[2].z-position.z)**2)
            force += FakeVector(
                -1 * term[1] * (relative_distance ** term[0]) * (term[2].x - position.x) / relative_distance,
                -1 * term[1] * (relative_distance ** term[0]) * (term[2].y - position.y) / relative_distance,
                -1 * term[1] * (relative_distance ** term[0]) * (term[2].z - position.z) / relative_distance
            )
        return force.vectorise()

    def get_acceleration(self, position: Vector, *args) -> Vector:
        """
        Computes the gradient of the scalar field at a given position using a step of size epsilon.

        Parameters
        ----------
        position : Vector
            The position where the gradient should be evaluated
        args :
            Arguments to match signature.

        Returns
        -------
        gradient : Vector
            The gradient at the desired position.
        """

        return self(position)
