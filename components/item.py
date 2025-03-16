#Itemklasse
class Item: 
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs): # kwargs ist quasi das selbe so wie ard
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs