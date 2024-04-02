from inspect import getsource, signature


class Lambda:
    """
    Wraps the lambda function to allow pickling.
    """
    def __init__(self, func: str, number_of_parameters: int):
        """
        Initialize a Lambda object.

        Parameters
        ----------
        func : str
            A function of 3 or 6 arguments, given in the form of a string representation of a lambda function. The
            first three are each simulated body's x, y, and z values and the last three, if present, are the tracked
            body's x, y, and z values.
            Examples:
            Lambda("lambda x, y, z, t_x, t_y, t_z: (1.3 < ((x-t_x)**2 + (y-t_y)**2)**0.5 < 1.7)", 6)
            Lambda("lambda x, y, z: (0 < x < 900) and (0 < y < 900)", 3)
        number_of_parameters : int
            Number of parameters of the provided function.
        """
        self.func_str = func
        self.number_of_parameters = number_of_parameters
        # Store the function as a string to allow pickling
        # self.func_str = getsource(func).rstrip().rstrip("),")
        # self.func_str = self.func_str[self.func_str.index("(")+1:]
        # self.number_of_parameters = len(signature(func).parameters)
    
    def __call__(self, *values):
        return eval(self.func_str)(*values)
    
    def __str__(self):
        return self.func_str
