from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.config import Config

from Core.Rendering.render_kivy import Scene
from Core.Rendering.render_kivy import SceneManager

from Core.Event.EventHandler import EventHandler
from Core.Event.EventHandler import WindowEventHandler

from kivy.core.window import Window

class Engine(App):
    """
    Game Engine entry point

    __init__ (self, game, **kwargs):
        game (Game) : game class to run
    
     """
    def __init__(self, game, **kwargs):
        KIVY_IMAGE='sdl2,pil'
        Config.set('graphics', 'width', '1280')
        Config.set('graphics', 'height', '720')
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.write()
        super(Engine, self).__init__(**kwargs)
        self.game = game
        self.title = game.title
        self.icon = game.icon
        self.run()

    def build(self):
        return Main(self.game)

class Main(Widget):

    instance = None

    def __init__(self, game, **kwargs):
        super(Main, self).__init__(**kwargs)
        Main.instance = self
        self.add_widget(EventHandler())
        self.game = game
        self.game_update = game.update
        self.scene = ''
        game.start()
        WindowEventHandler.window_close_request_callback.append(self.window_request_close)
        Clock.max_iteration = 60
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        if self.game_update : self.game_update(dt)

    def window_request_close(self, window, other=None):
        self.game.end()
    