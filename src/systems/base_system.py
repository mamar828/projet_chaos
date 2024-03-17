"""
    @file:              base_system.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create the basic structure of a many body system.
"""
from typing import Dict, List, Union, Optional
from copy import deepcopy

from numpy import abs, gradient, ones_like, rot90, zeros_like
from matplotlib.pyplot import close, colorbar, imshow, gca, scatter, show

from src.bodies.base_body import Body
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import FakeVector, Vector
from src.fields.scalar_field import ScalarField


class BaseSystem:
    """
    A class used to compute simulations on systems made of multiple bodies.
    """

    def __init__(self, list_of_bodies: List[Body], base_potential: Optional[ScalarField] = None, n: int = 0):
        """
        Defines the required parameters.

        Parameters
        ----------
        list_of_bodies : List[Body]
            A list of the bodies used to create the system.
        base_potential : Optional[ScalarField]
            A ScalarField object to define the source-less potential. Defaults to a constant and null potential.
        n : int
            The log base 10 of the space unit relative to the meter (e.g. 3 means 1000m or km and 6 means 10**6m or Mm).
        """
        self.n = n
        if base_potential is None:
            base_potential = ScalarField([(0, 0, Vector(0, 0, 0))])
        self._base_potential = base_potential
        self.fixed_bodies = []
        self.moving_bodies = []
        self.attractive_bodies = []
        self.list_of_bodies = list_of_bodies
        for body in list_of_bodies:
            if body.fixed:
                self.fixed_bodies.append(body)
            else:
                self.moving_bodies.append(body)
            if body.has_potential:
                self.attractive_bodies.append(body)
        print([(body, body.position) for body in self.list_of_bodies])

    def update(self, time_step: float, epsilon: float = 10**(-2)):
        """
        Updates the position and velocity of the bodies within the system according to a potential and time step.

        Parameters
        ----------
        time_step : float
            The time step during which the acceleration and velocity are considered constant, a smaller values gives
            more accurate results.
        epsilon : float
            The space interval with which the gradient is computed, a smaller value gives more accurate results,
            defaults to 10**(-3).
        """
        potential_field = deepcopy(self._base_potential)
        for body in self.attractive_bodies:
            potential_field += body.potential
        # print(self.attractive_bodies)
        # print(potential_field.terms)
        if len(potential_field.terms) > 2:
            potential_field -= ScalarField([(0, 0, Vector(0, 0, 0))])
        for body in self.moving_bodies:
            if body.has_potential:
                # print("before", potential_field.terms)
                acting_potential = deepcopy(potential_field) - body.potential
            else:
                acting_potential = deepcopy(potential_field)
            # print("after", acting_potential.terms)
            body(time_step, acting_potential*(10**(-self.n))**3, epsilon*10**(-self.n))

    def show(
            self,
            colours: Union[str, List[str]] = "r",
            show_potential: bool = False,
            show_bodies: bool = False,
            show_potential_null_slope_points: float = False,
            axes: Optional[Dict[str, int]] = None):
        """
        Shows the system as a collection of dots in 2D space. The size of the dots is linearly proportional to their
        mass.

        Parameters
        ----------
        colours : Union[str, List[str]]
            Either a one-character string defining the uniform color of all bodies or a list of one-character string to
            represent the bodies in multiple colours. If the length of the list is less than the number of bodies, the
            colours loop back and if it is longer only the first necessary colours are used. Defaults to monochromatic
            red.
        show_potential : bool
            Whether to show the potential field. Defaults to False.
        show_bodies : bool
            Whether to show the bodies. Defaults to False.
        show_potential_null_slope_points : bool
            Whether to show the approximate places where the potentials are at the extremum. Defaults to False.
        axes : Optional[List[str]]
            A list of the two axes to plot, defaults to x and y with 110% of the distance between the origin and the
            furthest point.
        """

        if axes is None:
            axes_names = ["x", "y"]
            axes_size = []
        else:
            axes_names, axes_size = list(axes.keys()), list(axes.values())
        list_of_masses, list_of_massive_bodies, list_of_massless_bodies = [], [], []
        first_axis_positions, second_axis_positions = [], []
        min_first_axis, max_first_axis = 10 ** 10, -10 ** 10
        min_second_axis, max_second_axis = 10 ** 10, -10 ** 10

        for body in self.list_of_bodies:
            if isinstance(body, GravitationalBody):
                list_of_masses.append(body.mass)
                list_of_massive_bodies.append(body)
            else:
                list_of_massless_bodies.append(body)

            x = getattr(body.position, axes_names[0])
            first_axis_positions.append(x)
            max_first_axis = x if x > max_first_axis else max_first_axis
            min_first_axis = x if x < min_first_axis else min_first_axis
            y = getattr(body.position, axes_names[1])
            second_axis_positions.append(y)
            max_second_axis = y if y > max_second_axis else max_second_axis
            min_second_axis = y if y < min_second_axis else min_second_axis

        if show_potential or show_potential_null_slope_points:
            potential_field = deepcopy(self._base_potential)
            for body in self.attractive_bodies:
                potential_field += body.potential

            stop = FakeVector(0, 0, 0)
            setattr(stop, axes_names[0], max_first_axis*1.1)
            setattr(stop, axes_names[1], max_second_axis*1.1)
            if len(axes_size) == 0:
                axes_size = [max_first_axis*1.1, max_second_axis*1.1]
            potential_array = potential_field.get_potential_field(
                Vector(0, 0, 0),
                stop.vectorise(),
                {k: v*5 for k in axes_names for v in axes_size},
                (0, 0, 0)
            )

            if show_potential:
                imshow(rot90(potential_array), cmap="binary", extent=(0, axes_size[0], 0, axes_size[1]))
                colorbar()

            if show_potential_null_slope_points:
                threshold = show_potential_null_slope_points
                x_gradient = gradient(potential_array, axis=0)
                y_gradient = gradient(potential_array, axis=1)

                x_mask = (abs(x_gradient) > threshold)
                y_mask = (abs(y_gradient) > threshold)

                overlay = ones_like(potential_array)
                null_overlay = zeros_like(potential_array)
                overlay[x_mask] = null_overlay[x_mask]
                overlay[y_mask] = null_overlay[y_mask]
                imshow(rot90(y_gradient), alpha=0.75, extent=(0, axes_size[0], 0, axes_size[1]))
                imshow(rot90(x_gradient), alpha=0.75, extent=(0, axes_size[0], 0, axes_size[1]))

                imshow(rot90(overlay), alpha=0.2, cmap="binary_r", extent=(0, axes_size[0], 0, axes_size[1]))

        if show_bodies:
            ax = gca()
            ax.set_xlim([0, max_first_axis*1.1])
            ax.set_ylim([0, max_second_axis*1.1])
            for i, body in enumerate(list_of_massive_bodies):
                scatter(
                    getattr(body.position, axes_names[0]),
                    getattr(body.position, axes_names[1]),
                    s=10,
                    c=colours[i % len(colours)]
                )

            for i, body in enumerate(list_of_massless_bodies):
                scatter(
                    getattr(body.position, axes_names[0]),
                    getattr(body.position, axes_names[1]),
                    s=10,
                    c=colours[(i + len(list_of_massive_bodies)) % len(colours)]
                )

        if show_bodies or show_potential_null_slope_points or show_potential:
            show()
            close()
