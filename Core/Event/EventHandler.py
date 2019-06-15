from kivy.core.window import Window
from kivy.uix.widget import Widget

class EventHandler(Widget):
    def __init__(self, **kwargs):
        super(EventHandler, self).__init__(**kwargs)
        self.add_widget(WindowEventHandler(), index=0)
        self.add_widget(KeyboardEventHandler(), index=1)

class KeyboardEventHandler(Widget):

    keyboard_press_down_callback = []
    keyboard_press_up_callback = []

    def __init__(self, **kwargs):
        super(KeyboardEventHandler, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, instance, keycode, *largs):
        for x in KeyboardEventHandler.keyboard_press_up_callback : x(instance,keycode, *largs)
        return True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        for x in KeyboardEventHandler.keyboard_press_down_callback : x(keyboard, keycode, text, modifiers)
        if keycode[1] == 'escape':
            keyboard.release()
        return True


class WindowEventHandler(Widget):
    window_show_callback = []
    window_hide_callback = []
    window_close_callback = []
    window_close_request_callback = [] 
    window_resize_callback = []
    window_draw_callback = []

    def __init__(self, **kwargs):
        super(WindowEventHandler, self).__init__(**kwargs)
        self._window = Window
        self._window.bind(on_show=self._window_show)
        self._window.bind(on_show=self._window_hide)
        self._window.bind(on_close=self._window_close)
        self._window.bind(on_request_close=self._window_request_close)
        self._window.bind(on_draw=self._window_draw)
        self._window.bind(on_resize=self._window_resize)
        self._window.bind(on_maximize=self._window_maximize)

    def _window_show(self, window):
        for x in WindowEventHandler.window_show_callback:
            x(self, window)
    def _window_hide(self, window):
        for x in WindowEventHandler.window_hide_callback:
            x(self, window)

    def _window_close(self, window):
        for x in WindowEventHandler.window_close_callback:
            x(self,window)
        self._unbind()

    def _window_request_close(self, window, **kargs):
        for x in WindowEventHandler.window_close_request_callback:
            x(self,window)
       

    def _window_resize(self, window, width, height):
        for x in WindowEventHandler.window_resize_callback:
            x( self, width, height)

        
    def _window_draw(self, window):
        for x in WindowEventHandler.window_draw_callback:
            x(self,window)

    def _window_maximize(self, window):
        self._window_resize(window, window.size[0], window.size[1])

    def _unbind(self):
        self._window.unbind(on_show=self._window_show)
        self._window.unbind(on_show=self._window_hide)
        self._window.unbind(on_close=self._window_close)
        self._window.unbind(on_request_close=self._window_request_close)
        self._window.unbind(on_draw=self._window_draw)
        self._window.unbind(on_resize=self._window_resize)