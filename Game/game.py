class Game(object):
    instance = None
    """ Abstract Game Class derive from this to create a new game """
    def __init__(self, **kwargs):
        Game.instance = self
        self.title = 'My Game'
        self.icon = ''
        self.maxfps = 0
        self.width = 1280
        self.height = 720
    def start(self):
        pass
    def update(self):
        pass
    def end(self):
        pass