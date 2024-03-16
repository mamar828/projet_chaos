"""
    @file:              base_system.py
    @Author:            Félix Desroches

    @Creation Date:     03/2024
    @Last modification: 03/2024

    @Description:       This file contains a class used to create the basic structure of a many body system.
"""

from typing import Dict, List, Union, Optional

import numpy as np
import matplotlib.pyplot as plt

from src.bodies.base_body import Body
from src.bodies.gravitational_body import GravitationalBody
from src.tools.vector import FakeVector, Vector
from src.fields.scalar_field import ScalarField


class BaseSystem:
    """
    A class used to compute simulations on systems made of multiple bodies.
    """

    def __init__(self, list_of_bodies: List[Body], base_potential: Optional[ScalarField] = None, n: int = 1):
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
        self.base_potential = base_potential
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

    def update(self, time_step: float, epsilon: float = 10**(-3)):
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
        potential_field = self.base_potential
        for body in self.attractive_bodies:
            potential_field += body.potential
        for body in self.moving_bodies:
            body(time_step, potential_field*(10**(-self.n))**3, epsilon)

    def show(
            self,
            colours: Union[str, List[str]] = "r",
            show_potential: bool = False,
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
            Whether to show the potential field as well as the bodies. Defaults to False. NB: If the potential is show,
            distances will be in pixels and thus relative while hiding the potential shows the distances given when
            creating the bodies.
        axes : Optional[List[str]]
            A list of the two axes to plot, defaults to x and y.
        """

        if axes is None:
            axes = {"x": 1000, "y": 1000}

        axes_names, axes_size = list(axes.keys()), list(axes.values())
        list_of_masses, list_of_massive_bodies, list_of_massless_bodies = [], [], []
        first_axis_positions, second_axis_positions = [], []
        min_first_axis, max_first_axis = 10 ** 10, -10 ** 10
        min_second_axis, max_second_axis = 10 ** 10, -10 ** 10

        if show_potential:
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

            potential_field = self.base_potential
            for body in self.attractive_bodies:
                potential_field += body.potential

            start = FakeVector(0, 0, 0)
            stop = FakeVector(0, 0, 0)
            setattr(start, axes_names[0], min_first_axis - (max_first_axis-min_first_axis)/10)
            setattr(start, axes_names[1], min_second_axis - (max_second_axis-min_second_axis)/10)
            setattr(stop, axes_names[0], max_first_axis + (max_first_axis-min_first_axis)/10)
            setattr(stop, axes_names[1], max_second_axis + (max_second_axis-min_second_axis)/10)
            x_min = getattr(start, axes_names[0])
            x_max = getattr(stop, axes_names[0])
            y_min = getattr(start, axes_names[1])
            y_max = getattr(stop, axes_names[1])
            for i, body in enumerate(list_of_massive_bodies):
                width = (x_max-x_min) if (x_max-x_min) > 0 else (y_max-y_min)
                height = (y_max - y_min) if (y_max - y_min) > 0 else (x_max - x_min)
                if (y_max-y_min) <= 0 and (x_max - x_min) <= 0:
                    height = 100
                    width = 100
                plt.scatter(
                    (getattr(body.position, axes_names[0]) - x_min)/width*axes_size[0],
                    list(axes.values())[1]-(getattr(body.position, axes_names[1]) - y_min)/height*axes_size[1],
                    s=body.mass/max(list_of_masses)*20,
                    c=colours[i % len(colours)]
                )

            for i, body in enumerate(list_of_massless_bodies):
                plt.scatter(
                    (getattr(body.position, axes_names[0]) - x_min)/(x_max-x_min)*axes_size[0],
                    list(axes.values())[1]-(getattr(body.position, axes_names[1]) - y_min)/(y_max-y_min)*axes_size[1],
                    s=10,
                    c=colours[(i + len(list_of_massive_bodies)) % len(colours)]
                )

            potential_array = potential_field.get_potential_field(
                start.vectorise(),
                stop.vectorise(),
                axes,
                (0, 0, 0)
            )

            plt.imshow(np.rot90(potential_array), cmap="binary")
            plt.colorbar()
            plt.show()
            plt.close()
        else:
            for body in self.list_of_bodies:
                if isinstance(body, GravitationalBody):
                    list_of_masses.append(body.mass)
                    list_of_massive_bodies.append(body)
                else:
                    list_of_massless_bodies.append(body)

            for i, body in enumerate(list_of_massive_bodies):
                plt.plot(
                    getattr(body.position, axes_names[0]),
                    getattr(body.position, axes_names[1]),
                    f"{colours[i % len(colours)]}o",
                    markersize=body.mass/max(list_of_masses)*5,
                )

            for i, body in enumerate(list_of_massless_bodies):
                plt.plot(
                    getattr(body.position, axes_names[0]),
                    getattr(body.position, axes_names[1]),
                    f"{colours[(i + len(list_of_massive_bodies)) % len(colours)]}o",
                    markersize=2.5,
                )
            plt.show()
            plt.close()
