from typing import Callable
from eztcolors import Colors as C

class Element3D:
    def __init__(
            self,
            texture: str | int="white",
            rotation: tuple[int,int,int]=(0,0,0),
            scale: tuple[int,int,int]=(1,1,1)
        ):
        self.texture = texture
        self.rotation = rotation
        self.scale = scale



class Object3D(Element3D):
    def __init__(
            self,
            texture: str | int = "white",
            rotation: tuple[int,int,int]=(0, 0, 0),
            scale: tuple[int,int,int]=(1,1,1),
            instance=None,
            model: str="sphere"
        ):
        """
        Initialize an Object3D object.

        Parameters
        ----------
        texture : str or int, optional
            Texture id of the object. Available texture ids can be found in textures.py. Defaults to "white".
        rotation : tuple[int,int,int], optional
            Rotation to apply to the object. Defaults to (0,0,0).
        scale : tuple[int,int,int], optional
            Scale to apply to the object. Defaults to (1,1,1).
        instance : object with a .update method.
            Function that determines the object's movement in the scene. Defaults to None.
        model : str, optional
            Specify the object's 3D model that should be used.
        """
        super().__init__(texture, rotation, scale)
        self.instance = instance
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
            save_filename: str=None
        ):
        """
        Initialize a Function3D object.

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
            Function of two variables that will determine the z value of the constructed plane. Defaults to None.
        resolution : tuple[int,int], optional
            Number of vertices constructed to represent the plane. The more the vertices, the more the smoothness of
            the plane. The first element corresponds to the resolution along the x axis and the second one, along the y
            axis. Defaults to (100,100).
        x_limits : tuple[int,int], optional
            Limits of the x values of the constructed plane. Defaults to (-100,100).
        y_limits : tuple[int,int], optional
            Limits of the y values of the constructed plane. Defaults to (-100,100).
        save_filename : str, optional
            If present, allows to quickly save and load the created vertices for later use. If the Function3D is used
            for the first time, the file will be created at the provided filename and the file will be loaded for every
            subsequent uses. The file's extension should be .gz. Defaults to None.
        """
        assert not save_filename or save_filename.endswith('.gz'), (
            f"{C.RED+C.BOLD}save_filename extension must be .gz, not {save_filename.split('.')[-1]}.{C.END}")
        super().__init__(texture, rotation, scale)
        self.position = position
        self.function = function
        self.resolution = resolution
        self.x_limits = x_limits
        self.y_limits = y_limits
        self.save_filename = save_filename
