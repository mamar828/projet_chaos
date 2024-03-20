from src.systems.base_system import BaseSystem


class ComputedSystem(BaseSystem):
    def update(self):
        """
        Updates the position of the bodies within the system according to their pre-computed positions.
        """
        for body in self.moving_bodies:
            body.update()
