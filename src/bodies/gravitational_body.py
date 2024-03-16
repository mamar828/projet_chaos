"""
    @file:              gravitational_body.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create a body with a mass used for computations using
                        gravitational potentials.
"""

from scipy.constants.constants import gravitational_constant

from src.bodies.base_body import Body
from src.fields.scalar_field import ScalarField
from src.tools.vector import Vector


class GravitationalBody(Body):
    """
    The basic class used to simulate a physical body. Bodies of this class are considered punctual and posses a
    position and velocity.
    """

    def __init__(
            self,
            mass: float,
            position: Vector,
            velocity: Vector = Vector(0, 0, 0),
            fixed: bool = False,
            has_potential: bool = True
    ):
        """
        Defines required parameters.

        Parameters
        ----------
        mass: float
            The mass of the body.
        position : Vector
            The position of the body when created.
        velocity : Vector
            The velocity of the body when created.
        fixed : bool
            Whether the body is fixed to it's initial position independent of all velocity and potentials.
        has_potential : bool
            Whether the body generates a potential field during simulations.
        """

        super().__init__(position, velocity, fixed, has_potential)
        if mass <= 0:
            raise ValueError("mass must be positive")
        self.mass = mass

    def __call__(self, time_step: float, potential: ScalarField, epsilon: float = 10**(-3)):
        """
        Updates the position and velocity of the body according to a potential and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller value gives
            more accurate results.
        potential : ScalarField
            The potential causing the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).
        """

        t = time_step
        x, y, z = self._position
        v_x, v_y, v_z = self._velocity
        # if self.has_potential:
        #     potential -= self.potential
        a_x, a_y, a_z = potential.get_gradient(self._position, epsilon)
        self._position = Vector(x+v_x*t-a_x/2*t**2, y+v_y*t-a_y/2*t**2, z+v_z*t-a_z/2*t**2)
        self._velocity = Vector(v_x-a_x*t, v_y-a_y*t, v_z-a_z*t)

    def update(self, time_step: float, potential: ScalarField, epsilon: float = 10**(-3)):
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
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).
        """

        self(time_step, potential, epsilon)

    @property
    def potential(self) -> ScalarField:
        """
        Gives the body's potential as a ScalarField object.

        Returns
        -------
        scalar_field : ScalarField
            The ScalarField object associated with the body's gravitational potential.
        """

        return ScalarField([(-1, -self.mass * gravitational_constant, self._position)])
