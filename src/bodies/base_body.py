"""
    @file:              base_body.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create the basic structure of a physical body used for
                        simulation.
"""
from copy import deepcopy
from warnings import filterwarnings
filterwarnings('ignore')

from src.fields.scalar_field import ScalarField
from src.tools.vector import Vector


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
            has_potential: bool,
            alive_position_threshold: float=2500,
            alive_velocity_threshold: float=10
    ):
        """
        Defines required parameters.

        Parameters
        ----------
        position : Vector
            The position of the body when created.
        velocity : Vector
            The velocity of the body when created.
        fixed : bool
            Whether the body is fixed to it's initial position independent of all velocity and potentials.
        has_potential : bool
            Whether the body generates a potential field during simulations.
        alive_position_threshold : float
            Maximum position in pixels for which the body is considered alive. Defaults to 5000 pixels.
        alive_position_threshold : float
            Maximum velocity for which the body is considered alive. Defaults to 10 units.
        """

        self._position = position
        self._velocity = velocity
        self._fixed = fixed
        self._has_potential = has_potential
        self.initial_position = deepcopy(position)
        self.initial_velocity = deepcopy(velocity)
        self.positions = [deepcopy(position)]
        self.alive_position_threshold = alive_position_threshold
        self.alive_velocity_threshold = alive_velocity_threshold

    def __call__(self, time_step: float, potential: ScalarField, epsilon: float):
        """
        Updates the position and velocity of the body according to a potential and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller values gives
            more accurate results.
        potential : ScalarField
            The potential causing the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results.
        """

        raise NotImplementedError

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
        Gives the body's potential as a ScalarField object.

        Returns
        -------
        scalar_field : ScalarField
            The ScalarField object associated with the body's potential.
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
    
    @property
    def is_dead(self) -> bool:
        """
        Gives whether the body is considered dead.

        Returns
        -------
        is_dead : bool
        """
        return (
            abs(self.position.x) > self.alive_position_threshold or 
            abs(self.position.y) > self.alive_position_threshold or 
            abs(self.position.z) > self.alive_position_threshold or 
            abs(self.velocity.x / self.initial_velocity.x) > self.alive_velocity_threshold or 
            abs(self.velocity.y / self.initial_velocity.y) > self.alive_velocity_threshold or 
            abs(self.velocity.z / self.initial_velocity.z) > self.alive_velocity_threshold
        )
