class Item:
    def __init__(self, use_function=None, **kwargs): # kwargs ist quasi das selbe so wie ard
        self.use_function = use_function
        self.function_kwargs = kwargs