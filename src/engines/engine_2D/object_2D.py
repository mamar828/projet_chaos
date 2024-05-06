from src.engines.engine_2D.models import *


class Object2D:
    def __init__(self,
            color: str | int = "white",
            position: tuple[int,int]=(0,0),
            scale: tuple[int,int]=(1,1),
            instance=None,
            plot_trace: bool=False,
            model: BaseModel=Circle
        ):
        self.color = color
        self.scale = scale
        self.position = position
        self.instance = instance
        self.plot_trace = plot_trace
        self.model = model
