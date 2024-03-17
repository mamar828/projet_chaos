import numpy as np

from src.systems.base_system import BaseSystem
from src.engines.engine_2D.engine import Engine_2D



class Simulation:
    def __init__(self, system: BaseSystem, maximum_delta_time: float=100):
        self.system = system
        self.maximum_delta_time = maximum_delta_time
        self.traces = None

    def show(self, *, traces: list=None, **params):
        """
        Show a simulation.

        Parameters
        ----------
        traces : list
            Optional, specify the bodies which should leave a trace.
        params : dict
            Parameters to pass to the Engine_2D class.
        """
        if not traces or len(traces) != len(self.system.list_of_bodies):
            self.traces = [None for i in range(len(self.system.list_of_bodies))]
        else:
            self.traces = traces
        app = Engine_2D(
            simulation=self,
            **params
        )
        app.run()

    def run(self): ...

    def save(self, foldername): ...

