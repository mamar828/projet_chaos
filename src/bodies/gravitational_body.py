from __future__ import annotations

from scipy.constants.constants import gravitational_constant
from eztcolors import Colors as C
from numpy.linalg import norm
from numpy.random import randint

from src.bodies.base_body import Body
from src.fields.scalar_field import ScalarField
from src.fields.vector_field import VectorField
from src.tools.vector import Vector
from src.simulator.lambda_func import Lambda


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
            integrator: str = "synchronous"
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
            Whether the body is fixed to it's initial position independent of velocity and potential.
        has_potential : bool
            Whether the body generates a potential field that acts on other bodies during simulations.
        integrator : str
            The type of integrator to use when updating the position of the body. Defaults to "synchronous". Currently
            implemented integrators are: "euler", "leapfrog", "synchronous", "kick-drift-kick", "yoshida", 
            "runge-kutta".
        """

        assert integrator in ["euler", "leapfrog", "synchronous", "kick-drift-kick", "yoshida", "runge-kutta", None], \
            ('The currently implemented integrators are:'
             ' "euler", "leapfrog", "synchronous", "kick-drift-kick", "yoshida", "runge-kutta"')
        self.integrator = integrator
        if integrator == "leapfrog":
            self.set_up_step = True
        elif integrator == "yoshida":
            w_0 = -2 ** (1 / 3) / (2 - 2 ** (1 / 3))
            w_1 = 1 / (2 - 2 ** (1 / 3))
            self.yoshida_c_constants = (w_1 / 2, (w_0 + w_1) / 2, (w_0 + w_1) / 2, w_1 / 2)
            self.yoshida_d_constants = (w_1, w_0, w_1)

        super().__init__(position, velocity, fixed, has_potential)
        if mass < 0:
            raise ValueError("mass must be positive")
        self.mass = mass
        self.dead = False   # Whether the body is dead or not and should be removed from the display
        self.time_survived = 0

    def __call__(
            self,
            time_step: float,
            field: ScalarField | VectorField,
            epsilon: float = 10 ** (-2),
            method: str = "potential"
    ) -> None:
        """
        Updates the position and velocity of the body according to an interaction field and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller value gives
            more accurate results.
        field : ScalarField | VectorField
            The interaction causing the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, defaults to 10**(-2).
        method : str
            The acceleration computation method, "potential" uses the gradient of the potential field and "force" uses
            a force field, defaults to "potential".
        """

        assert method in ["potential", "force"], 'The currently implemented methods are: "potential", "force"'

        self.time_survived += time_step
        x, y, z = self._position
        v_x, v_y, v_z = self._velocity
        if self.integrator != "yoshida":
            a_x, a_y, a_z = field.get_acceleration(self._position, epsilon)
        else:
            a_x, a_y, a_z = 0, 0, 0

        if self.integrator == "euler":
            self._position = Vector(
                x+v_x*time_step+a_x/2*time_step**2,
                y+v_y*time_step+a_y/2*time_step**2,
                z+v_z*time_step+a_z/2*time_step**2
            )
            self._velocity = Vector(v_x+a_x*time_step, v_y+a_y*time_step, v_z+a_z*time_step)

        elif self.integrator == "leapfrog":
            if self.set_up_step:
                v_x, v_y, v_z = v_x - a_x * time_step / 2, v_y - a_y * time_step / 2, v_z - a_z * time_step / 2
                self._velocity = Vector(v_x, v_y, v_z)
                self.set_up_step = False

            self._velocity = Vector(v_x + a_x * time_step, v_y + a_y * time_step, v_z + a_z * time_step)
            v_x, v_y, v_z = self._velocity
            self._position = Vector(x + v_x * time_step, y + v_y * time_step, z + v_z * time_step)

        elif self.integrator == "synchronous":
            self._position = Vector(
                x+v_x*time_step+a_x/2*time_step**2,
                y+v_y*time_step+a_y/2*time_step**2,
                z+v_z*time_step+a_z/2*time_step**2
            )
            new_a_x, new_a_y, new_a_z = field.get_acceleration(self._position, epsilon)
            self._velocity = Vector(
                v_x + (a_x + new_a_x) * time_step / 2,
                v_y + (a_y + new_a_y) * time_step / 2,
                v_z + (a_z + new_a_z) * time_step / 2
            )

        elif self.integrator == "kick-drift-kick":
            v_x, v_y, v_z = v_x + a_x * time_step / 2, v_y + a_y * time_step / 2, v_z + a_z * time_step / 2
            self._position = Vector(x + v_x * time_step, y + v_y * time_step, z + v_z * time_step)
            a_x, a_y, a_z = field.get_acceleration(self._position, epsilon)
            self._velocity = Vector(v_x + a_x * time_step / 2, v_y + a_y * time_step / 2, v_z + a_z * time_step / 2)

        elif self.integrator == "yoshida":
            c_1, c_2, c_3, c_4 = self.yoshida_c_constants
            d_1, d_2, d_3 = self.yoshida_d_constants

            x, y, z = x + c_1 * v_x * time_step, y + c_1 * v_y * time_step, z + c_1 * v_z * time_step
            a_x, a_y, a_z = field.get_acceleration(Vector(x, y, z), epsilon)
            v_x, v_y, v_z = v_x + d_1 * a_x * time_step, v_y + d_1 * a_y * time_step, v_z + d_1 * a_z * time_step

            x, y, z = x + c_2 * v_x * time_step, y + c_2 * v_y * time_step, z + c_2 * v_z * time_step
            a_x, a_y, a_z = field.get_acceleration(Vector(x, y, z), epsilon)
            v_x, v_y, v_z = v_x + d_2 * a_x * time_step, v_y + d_2 * a_y * time_step, v_z + d_2 * a_z * time_step

            x, y, z = x + c_3 * v_x * time_step, y + c_3 * v_y * time_step, z + c_3 * v_z * time_step
            a_x, a_y, a_z = field.get_acceleration(Vector(x, y, z), epsilon)
            v_x, v_y, v_z = v_x + d_3 * a_x * time_step, v_y + d_3 * a_y * time_step, v_z + d_3 * a_z * time_step

            self._position = Vector(x + c_4 * v_x * time_step, y + c_4 * v_y * time_step, z + c_4 * v_z * time_step)
            self._velocity = Vector(v_x, v_y, v_z)

        elif self.integrator == "runge-kutta":
            v_x_1, v_y_1, v_z_1 = v_x, v_y, v_z
            a_x_1, a_y_1, a_z_1 = a_x, a_y, a_z

            v_x_2, v_y_2, v_z_2 = (
                v_x + a_x_1 * 0.5 * time_step,
                v_y + a_y_1 * 0.5 * time_step,
                v_z + a_z_1 * 0.5 * time_step
            )
            a_x_2, a_y_2, a_z_2 = field.get_acceleration(Vector(
                x + v_x_1 * 0.5 * time_step,
                y + v_y_1 * 0.5 * time_step,
                z + v_z_1 * 0.5 * time_step
            ), epsilon)

            v_x_3, v_y_3, v_z_3 = (
                v_x + a_x_2 * 0.5 * time_step,
                v_y + a_y_2 * 0.5 * time_step,
                v_z + a_z_2 * 0.5 * time_step
            )
            a_x_3, a_y_3, a_z_3 = field.get_acceleration(Vector(
                x + v_x_2 * 0.5 * time_step,
                y + v_y_2 * 0.5 * time_step,
                z + v_z_2 * 0.5 * time_step
            ), epsilon)

            v_x_4, v_y_4, v_z_4 = (
                v_x + a_x_3 * time_step,
                v_y + a_y_3 * time_step,
                v_z + a_z_3 * time_step
            )
            a_x_4, a_y_4, a_z_4 = field.get_acceleration(Vector(
                x + v_x_3 * 0.5 * time_step,
                y + v_y_3 * 0.5 * time_step,
                z + v_z_3 * 0.5 * time_step
            ), epsilon)

            self._position = Vector(
                x + (v_x_1 + 2 * v_x_2 + 2 * v_x_3 + v_x_4) / 6 * time_step,
                y + (v_y_1 + 2 * v_y_2 + 2 * v_y_3 + v_y_4) / 6 * time_step,
                z + (v_z_1 + 2 * v_z_2 + 2 * v_z_3 + v_z_4) / 6 * time_step
            )
            self._velocity = Vector(
                v_x + (a_x_1 + 2 * a_x_2 + 2 * a_x_3 + a_x_4) / 6 * time_step,
                v_y + (a_y_1 + 2 * a_y_2 + 2 * a_y_3 + a_y_4) / 6 * time_step,
                v_z + (a_z_1 + 2 * a_z_2 + 2 * a_z_3 + a_z_4) / 6 * time_step
            )

    def update(
            self,
            time_step: float,
            field: ScalarField | VectorField,
            epsilon: float = 10 ** (-2),
            method: str = "potential"
    ) -> None:
        """
        Updates the position and velocity of the body according to an interaction field and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller value gives
            more accurate results.
        field : ScalarField | VectorField
            The interaction causing the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, defaults to 10**(-2).
        method : str
            The acceleration computation method, "potential" uses the gradient of the potential field and "force" uses
            a force field, defaults to "potential".
        """

        self(time_step, field, epsilon, method)

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """

        self.positions.append(self._position)

    @property
    def potential(self) -> ScalarField:
        """
        Gives the body's interaction as a ScalarField object.

        Returns
        -------
        scalar_field : ScalarField
            The ScalarField object associated with the body's interaction.
        """

        return ScalarField([(-1, -self.mass * gravitational_constant, self._position)])

    @property
    def gravitational_field(self) -> VectorField:
        """
        Gives the body's interaction as a VectorField object.

        Returns
        -------
        vector_field : VectorField
            The VectorField object associated with the body's interaction.
        """

        return VectorField([(-2, -self.mass * gravitational_constant, self._position)])
    
    def is_dead(
            self,
            potential: ScalarField,
            epsilon: float,
            potential_gradient_limit: float,
            body_alive_limits: Lambda,
            tracked_body: GravitationalBody = None
    ) -> bool:
        """
        Gives whether the body is considered dead by evaluating the modulus of the acceleration to which the body is
        subjected. Also checks if the body is too far away from its initial position.

        Parameters
        ----------
        potential : ScalarField
            Potential field to evaluate the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed.
        potential_gradient_limit: float
            Limit above which the body is considered dead.
        body_alive_limits: Lambda
            Lambda function specifying the conditions a body must respect to stay alive.
        tracked_body: GravitationalBody
            Body that is tracked in the system. This allows to make operations with that body to determine survival
            conditions.
            
        Returns
        -------
        is_dead : bool
            Whether the body is considered dead or alive.
        """

        if body_alive_limits:
            if body_alive_limits.number_of_parameters == 3:
                if not body_alive_limits(*self.position):
                    return True
            elif body_alive_limits.number_of_parameters == 6:
                if not body_alive_limits(*self.position, *tracked_body.position):
                    return True
            else:
                raise ValueError(C.RED + "Function has an incorrect number of parameters. Expected 3 or 6." + C.END)

        if norm([*potential.get_gradient(self._position, epsilon)]) > potential_gradient_limit:
            return True
        
        return False

    def get_color(self) -> tuple[int, int, int]:
        """
        Get a random color.

        Returns
        -------
        color : tuple[int, int, int]
            The random color.
        """

        return randint(0, 255, 3)

    def get_field(self, method: str) -> ScalarField | VectorField:
        """
        Gets the interaction in a specific form.

        Parameters
        ----------
        method : str
            The computation method, thus the form in which the interaction is required. The currently implemented
            methods are: "potential", "force".

        Returns
        -------
        field : calarField | VectorField
            The desired interaction
        """

        assert method in ["potential", "force"], 'The currently implemented methods are: "potential", "force"'

        if method == "force":
            return self.gravitational_field
        elif method == "potential":
            return self.potential
