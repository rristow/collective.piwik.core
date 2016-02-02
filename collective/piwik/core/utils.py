"""
Useful functions
"""

class DefaultDict(dict):
    """ A dictionary with a default value (such as 0 or [],
        or whatever you want) for unassigned keys
    """
    def __init__(self, list_or_dict=[],**kwds):
        super(DefaultDict, self).__init__(list_or_dict)
        self.update(kwds)
        self.default = None

    def __getitem__(self, key):
        return self.get(key, self.default)

    def __copy__(self):
        return DefaultDict(self.default, self)
