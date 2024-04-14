from __future__ import annotations

from scipy.constants import gravitational_constant
from numpy.linalg import norm
from numpy.random import randint
from numpy import sqrt
from eztcolors import Colors as C

from src.bodies.base_body import Body
from src.bodies.gravitational_body import GravitationalBody
from src.fields.scalar_field import ScalarField
from src.tools.vector import Vector, FakeVector
from src.simulator.lambda_func import Lambda


class NewBody(Body):
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
            Whether the body is fixed to it's initial position independent of all velocity and potentials.
        has_potential : bool
            Whether the body generates a potential field during simulations.
        integrator : str
            The type of integrator to use when updating the position of the body. Defaults to "synchronous". Currently
            implemented integrators are: "euler", "leapfrog", "synchronous", "kick-drift-kick", "yoshida", 
            "runge-kutta"
        """

        assert integrator in ["euler", "leapfrog", "synchronous", "kick-drift-kick", "yoshida", "runge-kutta"], \
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
        if mass <= 0:
            raise ValueError("mass must be positive")
        self.mass = mass
        self.acceleration = Vector(0, 0, 0)
        self.dead = False   # Whether the body is dead or not and should be removed from the display
        self.time_survived = 0
        # self.test_list = []

    def __call__(
            self,
            time_step: float,
            epsilon: float,
            bodies: list,
            n: int
    ) -> None:
        """
        Updates the position and velocity of the body according to a potential and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller value gives
            more accurate results.
        field : ScalarField
            The potential causing the body's acceleration.
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).
        """
        self.time_survived += time_step
        x, y, z = self._position
        v_x, v_y, v_z = self._velocity
        # if not self.has_potential: print("yes", self.position)
        a_x, a_y, a_z = self.get_acceleration(self._position, bodies, n, print_i=True)

        # self.test_list.append([self.time_survived, a_y])
        # if not self.has_potential: self.test_list.append([self.time_survived, self.get_acceleration(self._position, epsilon, time=self.time_survived)[1]])
        # elif 1.740e7 < self.time_survived < 1.75e7: print(self._position)
        # if not self.has_potential: self.test_list.append([self.time_survived, a_x])

        if self.integrator == "euler":
            self._position = Vector(
                x+v_x*time_step+a_x/2*time_step**2,
                y+v_y*time_step+a_y/2*time_step**2,
                z+v_z*time_step+a_z/2*time_step**2
            )
            self._velocity = Vector(v_x+a_x*time_step, v_y+a_y*time_step, v_z+a_z*time_step)

        elif self.integrator == "leapfrog":
            if self.set_up_step:
                v_x, v_y, v_z = self._velocity
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
            new_a_x, new_a_y, new_a_z = self.get_acceleration(self._position, bodies, n, print_i=True)
            # if not self.has_potential: print(f"{a_x:.5e} {a_y:.5e} {time_step:.5f}")
            self._velocity = Vector(
                v_x + (a_x + new_a_x) * time_step / 2,
                v_y + (a_y + new_a_y) * time_step / 2,
                v_z + (a_z + new_a_z) * time_step / 2
            )
            # if not self.has_potential: print(repr(self._velocity))
            # self.test_list.append([self.time_survived, a_x])

        elif self.integrator == "kick-drift-kick":
            v_x, v_y, v_z = v_x + a_x * time_step / 2, v_y + a_y * time_step / 2, v_z + a_z * time_step / 2
            self._position = Vector(x + v_x * time_step, y + v_y * time_step, z + v_z * time_step)
            a_x, a_y, a_z = self.get_acceleration(self._position, bodies, n)
            self._velocity = Vector(v_x + a_x * time_step / 2, v_y + a_y * time_step / 2, v_z + a_z * time_step / 2)

        elif self.integrator == "yoshida":
            c_1, c_2, c_3, c_4 = self.yoshida_c_constants
            d_1, d_2, d_3 = self.yoshida_d_constants

            x, y, z = x + c_1 * v_x * time_step, y + c_1 * v_y * time_step, z + c_1 * v_z * time_step
            a_x, a_y, a_z = self.get_acceleration(Vector(x, y, z), bodies, n)
            v_x, v_y, v_z = v_x + d_1 * a_x * time_step, v_y + d_1 * a_y * time_step, v_z + d_1 * a_z * time_step

            x, y, z = x + c_2 * v_x * time_step, y + c_2 * v_y * time_step, z + c_2 * v_z * time_step
            a_x, a_y, a_z = self.get_acceleration(Vector(x, y, z), bodies, n)
            v_x, v_y, v_z = v_x + d_2 * a_x * time_step, v_y + d_2 * a_y * time_step, v_z + d_2 * a_z * time_step

            x, y, z = x + c_3 * v_x * time_step, y + c_3 * v_y * time_step, z + c_3 * v_z * time_step
            a_x, a_y, a_z = self.get_acceleration(Vector(x, y, z), bodies, n)
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
            a_x_2, a_y_2, a_z_2 = self.get_acceleration(Vector(
                x + v_x_1 * 0.5 * time_step,
                y + v_y_1 * 0.5 * time_step,
                z + v_z_1 * 0.5 * time_step
            ), bodies, n)

            v_x_3, v_y_3, v_z_3 = (
                v_x + a_x_2 * 0.5 * time_step,
                v_y + a_y_2 * 0.5 * time_step,
                v_z + a_z_2 * 0.5 * time_step
            )
            a_x_3, a_y_3, a_z_3 = self.get_acceleration(Vector(
                x + v_x_2 * 0.5 * time_step,
                y + v_y_2 * 0.5 * time_step,
                z + v_z_2 * 0.5 * time_step
            ), bodies, n)

            v_x_4, v_y_4, v_z_4 = (
                v_x + a_x_3 * time_step,
                v_y + a_y_3 * time_step,
                v_z + a_z_3 * time_step
            )
            a_x_4, a_y_4, a_z_4 = self.get_acceleration(Vector(
                x + v_x_3 * 0.5 * time_step,
                y + v_y_3 * 0.5 * time_step,
                z + v_z_3 * 0.5 * time_step
            ), bodies, n)

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
        # if not self.has_potential: print("no", self.position)
        # if not self.has_potential: print(v_x, v_y)
        # print(x, y, z, self._position)
        # raise
        # if self.has_potential and 4.425e6 < self.time_survived < 4.6e6: print("potential", self.position)

    def update(self, time_step: float, epsilon: float, bodies: list, n):
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
        filtered_bodies = []
        for body in bodies:
            if body.position != self.position:
                # if self.has_potential: print(body.position, self.position)
                filtered_bodies.append(body)
        # if self.has_potential: print([body.position for body in filtered_bodies])
        # raise
        
        self(time_step, epsilon, filtered_bodies, n)

    def get_filtered_bodies(self, bodies: list) -> list:
        filtered_bodies = []
        for body in bodies:
            if body.position != self.position:
                filtered_bodies.append(body)
        return filtered_bodies

    def update_position(
            self,
            time_step: float,
            bodies: list,
            n: int
    ) -> None:
        filtered_bodies = self.get_filtered_bodies(bodies)
        self.time_survived += time_step
        x, y, z = self._position
        v_x, v_y, v_z = self._velocity
        self.acceleration = self.get_acceleration(self._position, filtered_bodies, n, print_i=True)
        a_x, a_y, a_z = self.acceleration

        self._position = Vector(
            x+v_x*time_step+a_x/2*time_step**2,
            y+v_y*time_step+a_y/2*time_step**2,
            z+v_z*time_step+a_z/2*time_step**2
        )

    def update_velocity(
            self,
            time_step: float,
            bodies: list,
            n: int
    ) -> None:
        filtered_bodies = self.get_filtered_bodies(bodies)
        v_x, v_y, v_z = self._velocity
        a_x, a_y, a_z = self.acceleration

        new_a_x, new_a_y, new_a_z = self.get_acceleration(self._position, filtered_bodies, n, print_i=True)
        self._velocity = Vector(
            v_x + (a_x + new_a_x) * time_step / 2,
            v_y + (a_y + new_a_y) * time_step / 2,
            v_z + (a_z + new_a_z) * time_step / 2
        )

    def get_acceleration(self, position: Vector, bodies: list, n, print_i=None):
        x_accel, y_accel, z_accel = 0, 0, 0
        for body in bodies:
            # if self.has_potential and print_i: print(body.position)
            # if self.has_potential and self.time_survived < 15000: print(body.position)
            x_dist = body.position.x*10**n-position.x*10**n
            y_dist = body.position.y*10**n-position.y*10**n
            z_dist = body.position.z*10**n-position.z*10**n
            relative_distance = sqrt(x_dist**2 + y_dist**2 + z_dist**2)
            total_accel = gravitational_constant * body.mass / relative_distance**2
            x_accel += total_accel * x_dist / relative_distance
            y_accel += total_accel * y_dist / relative_distance
            z_accel += total_accel * z_dist / relative_distance
            # if not self.has_potential and 1.75e7 < self.time_survived < 2e7 and print_i:
            #     print(self.time_survived, total_accel * y_dist / relative_distance * 10**(-n), position, body.position)
        return x_accel * 10**(-n), y_accel * 10**(-n), z_accel * 10**(-n)

    def save_position(self):
        """
        Saves the current position of the body to the positions list.
        """
        self.positions.append(self._position)

    def is_dead(
            self,
            potential: ScalarField,
            epsilon: float,
            potential_gradient_limit: float,
            body_alive_limits: Lambda,
            tracked_body: GravitationalBody=None
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
        potential_gradient_limit: float
            Quantity over which the body is considered dead.
        body_alive_func: Lambda
            Lambda function specifying the conditions a body must respect to stay alive.
        tracked_body: GravitationalBody
            Body that is tracked in the system. This allows to make operations with that body to determine alive
            conditions.
            
        Returns
        -------
        is_dead : bool
            Whether the body is considered dead or not.
        """
        if body_alive_limits:
            if body_alive_limits.number_of_parameters == 3:
                if not body_alive_limits(*self.position): return True
            elif body_alive_limits.number_of_parameters == 6:
                if not body_alive_limits(*self.position, *tracked_body.position): return True
            else:
                raise ValueError(C.RED + "Function has an incorrect number of parameters. Expected 3 or 6." + C.END)

        # if norm([*potential.get_gradient(self._position, epsilon)]) > potential_gradient_limit: return True
        
        return False

    def get_color(self) -> tuple[int, int, int]:
        """
        Get a random color of the body.

        Returns
        -------
        color : tuple[int, int, int]
            The color of the body.
        """
        return randint(0, 255, 3)
