class Game(object):
    """ Abstract Game Class derive from this to create a new game """
    def __init__(self, **kwargs):
        self.title = 'My Game'
        self.icon = ''
    def start(self):
        pass
    def update(self):
        pass
    def end(self):
        pass