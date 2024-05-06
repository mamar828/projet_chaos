from src.tools.vector import Vector


class Field:
    """
    A class used to compute and define a field.
    """

    def __add__(self, other):
        """
        Adds two fields together.
        """

        raise NotImplementedError

    def __sub__(self, other):
        """
        Subtracts the second field's values from the first.
        """

        raise NotImplementedError

    def __call__(self, position: Vector):
        """
        The definition of this function depends on the type of field.
        """

        raise NotImplementedError
