from __future__ import annotations

from copy import deepcopy
from warnings import filterwarnings

from src.fields.scalar_field import ScalarField
from src.fields.vector_field import VectorField
from src.tools.vector import Vector

filterwarnings('ignore')


class Body:
    """
    The basic class used to simulate a physical body. Bodies of this class are considered punctual and posses a
    position and velocity.
    """

    def __init__(
            self,
            position: Vector,
            velocity: Vector,
            fixed: bool,
            has_potential: bool
    ):
        """
        Defines required parameters.

        Parameters
        ----------
        position : Vector
            The position of the body when created at time t=0.
        velocity : Vector
            The velocity of the body when created at time t=0.
        fixed : bool
            Whether the body is fixed to it's initial position independent of velocity and potential.
        has_potential : bool
            Whether the body generates a potential field that acts on other bodies during simulations.
        """

        self._position = position
        self._velocity = velocity
        self._fixed = fixed
        self._has_potential = has_potential
        self.initial_position = deepcopy(position)
        self.initial_velocity = deepcopy(velocity)
        self.positions = [deepcopy(position)]

    def __call__(
            self,
            time_step: float,
            field: ScalarField | VectorField,
            epsilon: float,
            method: str
    ):
        """
        Updates the position and velocity of the body according to a potential and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller values gives
            more accurate results.
        field : ScalarField | VectorField
            The potential causing the body's acceleration or the force field resulting from it.
        epsilon : float
            The space interval with which the gradient is computed.
        """

        raise NotImplementedError
    
    def __str__(self):
        return (f"fixed: {self.fixed}, has_potential: {self.has_potential}, " + 
                f"initial_position: {self.initial_position}, initial_velocity: {self.initial_velocity}")
    
    @property
    def fixed(self) -> bool:
        """
        Returns the fixed or movable state of the body.

        Returns
        -------
        fixed : bool
            The body's mouvement state.
        """

        return self._fixed

    @property
    def has_potential(self) -> bool:
        """
        Returns the potential generation state.

        Returns
        -------
        has_potential : bool
            The body's potential generation state.
        """

        return self._has_potential

    @property
    def potential(self) -> ScalarField:
        """
        Gives the body's interaction as a ScalarField object.

        Returns
        -------
        scalar_field : ScalarField
            The ScalarField object associated with the body's interaction.
        """

        raise NotImplementedError

    @property
    def gravitational_field(self) -> VectorField:
        """
        Gives the body's interaction as a VectorField object.

        Returns
        -------
        vector_field : VectorField
            The VectorField object associated with the body's interaction.
        """

        raise NotImplementedError

    @property
    def position(self) -> Vector:
        """
        Gives the body's position as a Vector object.

        Returns
        -------
        position : Vector
            The body's position.
        """

        return self._position

    @property
    def velocity(self) -> Vector:
        """
        Gives the body's velocity as a Vector object.

        Returns
        -------
        velocity : Vector
            The body's velocity.
        """

        return self._velocity
