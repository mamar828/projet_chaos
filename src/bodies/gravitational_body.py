"""
    @file:              gravitational_body.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create a body with a mass used for computations using
                        gravitational potentials.
"""

from scipy.constants.constants import gravitational_constant
from numpy.linalg import norm

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
            has_potential: bool = True,
            alive_position_threshold: float=5000,
            alive_velocity_threshold: float=10
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
        alive_position_threshold : float
            Maximum position in pixels for which the body is considered alive. Defaults to 5000 pixels.
        alive_velocity_threshold : float
            Maximum velocity for which the body is considered alive. Defaults to 10 units.
        """

        super().__init__(position, velocity, fixed, has_potential,
                         alive_position_threshold, alive_velocity_threshold)
        if mass <= 0:
            raise ValueError("mass must be positive")
        self.mass = mass
        self.dead = False   # Whether the body is dead or not and should be removed from the display

    def __call__(self, time_step: float, potential: ScalarField, epsilon: float = 10**(-2)):
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

        x, y, z = self._position
        v_x, v_y, v_z = self._velocity
        a_x, a_y, a_z = potential.get_gradient(self._position, epsilon)
        self._position = Vector(
            x+v_x*time_step-a_x/2*time_step**2,
            y+v_y*time_step-a_y/2*time_step**2,
            z+v_z*time_step-a_z/2*time_step**2
        )
        self._velocity = Vector(v_x-a_x*time_step, v_y-a_y*time_step, v_z-a_z*time_step)

    def update(self, time_step: float, potential: ScalarField, epsilon: float = 10**(-2)):
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

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """
        self.positions.append(self._position)

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
    
    def is_dead(self,
        potential: ScalarField,
        epsilon: float,
        potential_gradient_limit: int,
        body_position_limit: tuple[int,int]
    ) -> bool:
        """
        Gives whether the body is considered dead by evaluating if the modulus of the acceleration to which the body is
        subjected. Also checks if the body is too far away from its initial position.

        Parameters
        ----------
        potential : ScalarField
            Potential field to evaluate the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
        potential_gradient_limit: int
            Quantity over which the body is considered dead.
        body_position_limit: tuple[int,int]
            Specify the position in pixels of a body to be considered still alive.
            
        Returns
        -------
        is_dead : bool
            Whether the body is considered dead or not.
        """
        condition_2D = (
            norm([*potential.get_gradient(self._position, epsilon)]) > potential_gradient_limit or
                body_position_limit[0]-0.1 > self.position.x or self.position.x > body_position_limit[1] or 
                body_position_limit[0]-0.1 > self.position.y or self.position.y > body_position_limit[1]
        )
        if self.position.z == 0:
            return condition_2D
        else:
            return (condition_2D or 
                    body_position_limit[0]-0.1 > self.position.z or self.position.z > body_position_limit[1])

