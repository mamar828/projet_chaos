from pygame.font import SysFont

from src.engines.engine_2D.models import *
from src.systems.computed_system import ComputedSystem

# from numpy import arctan, pi


class Scene:
    def __init__(self, app, display_clock: bool, clock_font: tuple[tuple, str]):
        self.app = app
        self.system = app.simulation.system
        self.display_clock = display_clock
        self.clock_sys_font = SysFont(*clock_font[0])
        self.clock_color = clock_font[1]
        self.objects = []
        self.load()

    def load(self):
        # Determine the displayed colors
        if isinstance(self.system, ComputedSystem):
            color_func = lambda body: body.get_color()
        else:
            # A lambda function is also created only for consistency
            color_func = lambda body: BaseModel.get_random_color()
        
        for body, plot_trace in zip(self.system.list_of_bodies, self.app.simulation.traces):
            s = round(body.mass/(2*10**30), 0) * 30 + 10
            # s = 2*5*arctan(float(body.mass))/pi
            self.objects.append(Circle(screen=self.app.screen, color=color_func(body), scale=(s,s),
                                position=(body.position[0], body.position[1]), instance=body, plot_trace=plot_trace))

    @staticmethod
    def format_time(time: int) -> str:
        years = int(time // (3600*24*365))
        days = int(time % (3600*24*365) // (3600*24))
        hours = int(time % (3600*24*365) % (3600*24) // (3600))
        minutes = int(time % (3600*24*365) % (3600*24) % (3600) // 60)
        seconds = int(time % (3600*24*365) % (3600*24) % (3600) % 60)
        return f"{years}y {days}d {hours:02}:{minutes:02}:{seconds:02}"

    def update(self):
        # Update system
        for i in range(int(self.app.delta_time // self.app.simulation.maximum_delta_time)):
            self.system.update(self.app.simulation.maximum_delta_time)
        self.system.update(self.app.delta_time % self.app.simulation.maximum_delta_time)

        # Update display
        for obj in self.objects:
            if not obj.instance.dead:
                obj.move((obj.instance.position[0], obj.instance.position[1]))
                obj.update()
            else:
                obj.destroy()
                self.objects.remove(obj)
        
        # Update clock
        if self.display_clock:
            time = self.clock_sys_font.render(f"{self.format_time(self.app.simulation_time)}", True, self.clock_color)
            self.app.screen.blit(time, (self.app.screen.get_width() - time.get_width() - 10, 10))

    def destroy(self):
        del self
