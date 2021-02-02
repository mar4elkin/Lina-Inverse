class EmptyString(Exception):

    def __init__(self, ctr, message="String can't be empty"):
        self.ctr = ctr
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.ctr} -> {self.message}'

class BattleTagAlready(Exception):

    def __init__(self, ctr, message="That battle tag already added"):
        self.ctr = ctr
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.ctr} -> {self.message}'

class ImageGenAttr(Exception):

    def __init__(self, *args):
            self.message = 'The passed attribute is not in the list'
            self.value = args[0]
            
    def __str__(self):
        if (self.message != None):
            return f'{self.value} -> {self.message}'
