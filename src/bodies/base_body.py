"""
    @file:              base_body.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create the basic structure of a physical body used for
                        simulation.
"""

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
            fixed: bool
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
        """

        self._position = position
        self._velocity = velocity
        self._fixed = fixed

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
