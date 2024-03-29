from typing import Callable
from eztcolors import Colors as C

from src.systems.computed_system import ComputedSystem
from src.tools.vector import Vector


class Element3D:
    def __init__(
            self,
            texture: str | int="white",
            position: tuple[int,int,int]=(0,0,0),
            rotation: tuple[int,int,int]=(0,0,0),
            scale: tuple[int,int,int]=(1,1,1),
            instance=None
        ):
        self.texture = texture
        self.rotation = rotation
        self.scale = scale
        self.position = position
        self.instance = instance


class Object3D(Element3D):
    def __init__(
            self,
            texture: str | int = "white",
            position: tuple[int,int,int]=(0,0,0),
            rotation: tuple[int,int,int]=(0,0,0),
            scale: tuple[int,int,int]=(1,1,1),
            instance=None,
            model: str="sphere"
        ):
        """
        Initialize an Object3D object. All coordinates are given in tuples of x, y, z.

        Parameters
        ----------
        texture : str or int, optional
            Texture id of the object. Available texture ids can be found in textures.py. Defaults to "white".
        position : tuple[int,int,int], optional
            Position of the object's origin if no instance is provided. Otherwise, the instance.get_position method is
            called to determine the object's center coordinates. Defaults to (0,0,0).
        rotation : tuple[int,int,int], optional
            Rotation to apply to the object. Defaults to (0,0,0).
        scale : tuple[int,int,int], optional
            Scale to apply to the object. Defaults to (1,1,1).
        instance : object with a .update method
            Function that determines the object's movement in the scene. Defaults to None.
        model : str, optional
            Specify the object's 3D model that should be used.
        """
        super().__init__(texture, position, rotation, scale, instance)
        self.model = model


class Function3D(Element3D):
    def __init__(
            self,
            texture: str | int="white",
            position: tuple[int,int,int]=(0,0,0),
            rotation: tuple[int,int,int]=(0,0,0),
            scale: tuple[int,int,int]=(1,1,1),
            function: Callable=None,
            resolution: tuple=(100,100),
            x_limits: tuple=(-100,100),
            y_limits: tuple=(-100,100),
            instance: ComputedSystem=None,
            save_filename: str=None
        ):
        """
        Initialize a Function3D object. All coordinates are given in tuples of x, y, z.

        Parameters
        ----------
        texture : str or int, optional
            Texture id of the function. Available texture ids can be found in textures.py. Defaults to "white".
        position : tuple[int,int,int], optional
            Position of the function's origin. Defaults to (0,0,0).
        rotation : tuple[int,int,int], optional
            Rotation to apply to the function. Defaults to (0,0,0).
        scale : tuple[int,int,int], optional
            Scale to apply to the function. Defaults to (1,1,1).
        function : Callable, optional
            Function of two variables that will determine the z value of the constructed plane, that will stay
            motionless. A single function or instance should be provided. Defaults to None.
        resolution : tuple[int,int], optional
            Number of vertices constructed to represent the plane. The more the vertices, the more the smoothness of
            the plane. The first element corresponds to the resolution along the x axis and the second one, along the y
            axis. Defaults to (100,100).
        x_limits : tuple[int,int], optional
            Limits of the x values of the constructed plane. Defaults to (-100,100).
        y_limits : tuple[int,int], optional
            Limits of the y values of the constructed plane. Defaults to (-100,100).
        instance : ComputedSystem, optional
            Gives the instance of the system whose potential should be plotted continuously. A single function or
            instance should be provided. Defaults to None.
        save_filename : str, optional
            If present, allows to quickly save and load the created vertices for later use. If the Function3D is used
            for the first time, the file will be created at the provided filename and the file will be loaded for every
            subsequent uses. The file's extension should be .gz. Defaults to None.
        """
        assert not save_filename or save_filename.endswith('.gz'), (
            f"{C.RED+C.BOLD}save_filename extension must be .gz, not {save_filename.split('.')[-1]}.{C.END}")
        assert function != instance, (f"{C.RED+C.BOLD}Only a function or an instance should be passed as "
                                             f"an argument, not both.{C.END}")
        super().__init__(texture, position, rotation, scale, instance)
        self.function = function
        self.resolution = resolution
        self.x_limits = x_limits
        self.y_limits = y_limits
        self.save_filename = save_filename
        if instance:
            # self.i = 0
            self.update()

    def update(self):
        # self.i += 1
        self.function = lambda x, y: self.instance.get_potential_function()(Vector(x,y,0)) * 1e10# + self.i
