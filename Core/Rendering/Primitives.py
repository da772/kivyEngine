from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics.instructions import InstructionGroup
from kivy.clock import Clock

from kivy.graphics import Color as _Color
from kivy.graphics import Rectangle as _Rectangle
from kivy.uix.image import Image as _Image
from kivy.uix.image import AsyncImage as _AsyncImage
from kivy.uix.label import Label as _Label
from kivy.uix.button import Button as _Button
from kivy.clock import Clock

from kivy.core.audio import SoundLoader as _SoundLoader

from Core.Event.EventHandler import EventHandler
from Core.Event.EventHandler import WindowEventHandler
from Core.Event.EventHandler import KeyboardEventHandler

from time import time

from queue import PriorityQueue



class SceneManager():
    """ Manage Scenes this manager allows for multiple \"Levels\" in a single game which can be swapped """
    SceneDict = {}

    @staticmethod
    def SetActive(name):
        """ Set a current scene to be active by name
            
            Attributes:
                name (string): name of scene to be active as a string
         """
        from Core.EntryPoint import Main
        if name in SceneManager.SceneDict :
            curScene = SceneManager.Get(Main.instance.scene)
            if curScene:
                 Main.instance.remove_widget(curScene)
                 curScene.setActive_event(False)
            Main.instance.scene = name
            Main.instance.add_widget(SceneManager.Get(name))
            SceneManager.Get(name).setActive_event(True)

    @staticmethod
    def Get(name):
        """ Get reference to scene by name

            Attributes:
                name (string): name of scene to get returns None if not
                found
        """
        return SceneManager.SceneDict[name] if name in SceneManager.SceneDict else None

    @staticmethod
    def Create(name, active=True):
        """ Create a new scene

            Attributes:
                name (string): name for the scene
                active (bool, true): should the new scene be the active
                scene
        """
        from Core.EntryPoint import Main
        s = Scene(name)
        SceneManager.SceneDict[name] = s
        if active : SceneManager.SetActive(name)
        return s


    @staticmethod 
    def Destroy(name, newScene=''):
        """ Destroy a scene by name

            Attributes:
                name (string): name of the scene to destroy
                newScene (string, ''): name of the scene to set active 
                after destroying leave blank to replace with new
                scene
        """
        import gc
        from Core.EntryPoint import Main
        if newScene is '':
            Main.instance.remove_widget(SceneManager.SceneDict[name])
            SceneManager.SceneDict[name].setActive_event(False)
            SceneManager.SceneDict[name].destroy()
            SceneManager.SceneDict.pop(name)  
            gc.collect()
        else:
            SceneManager.SetActive(newScene)
            Main.instance.remove_widget(SceneManager.SceneDict[name])
            SceneManager.SceneDict[name].setActive_event(False)
            SceneManager.SceneDict[name].destroy()
            SceneManager.SceneDict.pop(name)
            gc.collect()
            return SceneManager.SceneDict[newScene]

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

""" Refactor kivy Primitives """
class Color(_Color):
    def __init___(self,**kwargs):
        super(Color, self).__init__(**kwargs)

class Image(_Image):
    def __init___(self,**kwargs):
        super(Image, self).__init__(**kwargs)

    def GetFrames(self):
        return self._coreimage.image.textures

class AsyncImage(_AsyncImage):
    def __init___(self,**kwargs):
        super(AsyncImage, self).__init__(**kwargs)

    def GetFrames(self):
        return self._coreimage.image.textures

class Rectangle(_Rectangle):
    def __init___(self,**kwargs):
        super(Rectangle, self).__init__(**kwargs)

class Button(_Button):
    def __init___(self,**kwargs):
        super(Button, self).__init__(**kwargs)

class Label(_Label):
    def __init___(self,**kwargs):
        super(Label, self).__init__(**kwargs)

        SoundLoader
class SoundLoader(_SoundLoader):
    def __init___(self,**kwargs):
        super(SoundLoader, self).__init__(**kwargs)
     

class Scene(Widget):
    """ Contain display actors and ui acts as a Level for game
    
        Attributes:
            name (string): unique name identifier
            **kwargs (**kwargs): additional arguments
      """
    def __init__(self, name,**kwargs):
            super(Scene, self).__init__(**kwargs)
            WindowEventHandler.window_resize_callback.append(self.resizeScene_callback)
            self.widget_draw = PriorityQueue()
            self.widget_list = {}
            self.collision_widget_list = []
            self.collision_list = {}
            self.resize_event = []
            self.name = name
            self.lastTime = 0
            self.frameCounter = 0
            self.fps = 0
            self.cameraPos = (0,0)
            self.collisionThread = None
            self.renderThread = None
            self.cameraPosUnscaled = (0,0)
            self.size = (Window.size[0], Window.size[1])
            self.on_setActive = []
            self.kUpFunc = None
            self.kDownFunc = None
            self.setCameraPos((0,0)) 

    def setKeyboardPressUpCallback(self, func):
        """ Function to pass keyboard press up callback to
        
            Attributes:
                func (function (instance, keycode, *largs) ) :
                function to call on key press up
         """
        self.kUpFunc = func
        KeyboardEventHandler.keyboard_press_up_callback.append(func)

    def setKeyboardPressDownCallback(self, func):
        """ Function to pass keyboard press up callback to
        
            Attributes:
                func (function (keyboard, keycode, text, modifiers) ) :
                function to call on key press down
         """
        self.kDownFunc = func
        KeyboardEventHandler.keyboard_press_down_callback.append(func)

    def setActive_event(self, b):
        """ on scene set Active  """
        from Core.EntryPoint import Main
        for x in self.on_setActive: x(b)
        if b:
            if not self.collisionThread : self.collisionThread = Clock.schedule_interval(self.__check_collision__, 1.0/30)
            if not self.renderThread : self.renderThread = Clock.schedule_interval(self.__render__, 0 if Main.instance.maxfps is 0 else 1/Main.instance.maxfps )
            if self.kUpFunc is not None and self.kUpFunc not in KeyboardEventHandler.keyboard_press_up_callback: 
                KeyboardEventHandler.keyboard_press_up_callback.append(self.kUpFunc)
            if self.kDownFunc is not None and self.kDownFunc not in KeyboardEventHandler.keyboard_press_down_callback :
                KeyboardEventHandler.keyboard_press_down_callback.append(self.kDownFunc)
        else:
            if self.collisionThread : 
                Clock.unschedule(self.collisionThread)
                self.collisionThread = None
            if self.renderThread : 
                Clock.unschedule(self.renderThread)
                self.renderThread = None
            if self.kUpFunc in KeyboardEventHandler.keyboard_press_up_callback: 
                KeyboardEventHandler.keyboard_press_up_callback.remove(self.kUpFunc)
            if self.kDownFunc in KeyboardEventHandler.keyboard_press_down_callback :
                KeyboardEventHandler.keyboard_press_down_callback.remove(self.kDownFunc)

    def __check_collision__(self, dt):
        """ check collision of scene actors call collision start, on colliding, and collision end """
        to_remove = []
        for x in self.collision_list.keys():
            if not self.collision_list[x][0].collide_widget(self.collision_list[x][1]):
                self.collision_list[x][0].__on_collision_end__(self.collision_list[x][1])
                to_remove.append(x)

        while len(to_remove):
            self.collision_list.pop(to_remove.pop())

        for x in self.collision_widget_list:
            for y in self.collision_widget_list:
                if x is not y and x.collide_widget(y):
                    s = "{}-{}".format(id(x),id(y))
                    if s not in self.collision_list.keys():
                        self.collision_list.update( {s : (x,y) } )
                        x.__on_collision_start__(y)
                    x.__on_collision__(y)
        pass

    def Clear(self):
        import gc
        v = list(self.widget_list.values())
        while len(v):
            w = v.pop().group
            w.destroy()
        self.collision_list.clear()
        self.collision_widget_list.clear()
        gc.collect()
        pass

    def __add_collision__(self, w):
        """ add actor to collision group """
        if w not in self.collision_widget_list:
            self.collision_widget_list.append(w)

    def __remove_collision__(self, w):
        """ remove actor from collision group """
        if w in self.collision_widget_list:
            self.collision_widget_list.remove(w)

    def isActive(self):
        """ Check if scene is the active scene returns bool """
        return True if self.parent else False

    def __add_widget__(self, w):
        """ add widget to scene using priority queue """
        self.widget_list.update(  {w.group : w}  )
        if w.group.collision and w.group not in self.collision_widget_list : self.collision_widget_list.append(w.group)
        for x in self.widget_list.values() : self.widget_draw.put(x)
        self.clear_widgets()
        while not self.widget_draw.empty():
            w = self.widget_draw.get()
            self.add_widget(w.group)

    def __remove_widget__(self, w):
        """ remove widget from scene  """
        self.widget_list.pop(w)
        if w.collision and w in self.collision_widget_list: self.collision_widget_list.remove(w)
        for x in self.widget_list.values() : self.widget_draw.put(x)
        self.clear_widgets()
        while not self.widget_draw.empty():
            self.add_widget(self.widget_draw.get().group)

    def __render__(self, dt):
        """ render all actors in scene """
        v = self.widget_list.values()
        for x in  v : x.group.__main_render__()
        t = time()
        if t -self.lastTime >= 1.0 or self.lastTime is 0:
            self.fps = self.frameCounter
            self.frameCounter = 0
            self.lastTime = t
        else: self.frameCounter += 1
        pass

    def destroy(self):
        self.clear_widgets()
        v = list(self.widget_list.values())
        while len(v):
            w = v.pop().group
            w.destroy()
        WindowEventHandler.window_resize_callback.remove(self.resizeScene_callback)
        del self.widget_draw
        del self.widget_list
        del self.kDownFunc
        del self.kUpFunc
        del self.collision_widget_list
        del self.collision_list
        del self.resize_event
        del self.on_setActive

    def CreateActor(self, t,p=0, args={}):
        """ Create actor in current scene

            Attributes:
                t (Class): Class of actor to instantiate deriving
                from the Actor class
                p (int): drawing order
            Usage:
                scene.CreateActor(Actor, 2)
                Actors that derive from the UI class are draw on 
                top of regular actors
        """
        if issubclass(t, UI) :
            a = type(t.__class__.__name__, (t,), {})(self,p,args)
            g = GroupInstructionQueue(p, a)
            self.__add_widget__(g)
        else :
            a = type(t.__class__.__name__, (t,), {})(self,p+1000,args)
            g = GroupInstructionQueue( p+1000, a )
            self.__add_widget__(g)
        return a

    def resizeScene_callback(self, window, x, y):
        """ called on window resize """
        self.size = (x,y)
        for x in self.resize_event: x(x,y)

    def __camera_change__(self):
        """ called on camera pos change """
        self.resizeScene_callback(None, self.size[0], self.size[1])

    def setCameraPos(self, p):
        """ Set object position """
        self.cameraPosUnscaled = p
        self.cameraPos = ((p[0]/100)*self.size[0],(p[1]/100)*self.size[1])
        self.__camera_change__()

    def setCameraPosScaled(self, p):
        """ set object position relative to window """
        self.cameraPosUnscaled = (   ( (100*p[0] )/self.size[0] - 50  
        ,     (100*p[1] )/self.size[1] - 50 )  )
        self.setCameraPos(self.cameraPosUnscaled)


class Actor(Widget):
    """ Abstraction of simple Actor Renderer class
    """
    def __init__(self, scene, priority, args, **kwargs):
        """ Actor constructor """
        super(Actor, self).__init__(**kwargs)
        keys = args.keys()
        self.size = (0,0)
        self.frame_counter = 0
        self.collision = False
        self.debug = False
        self.sizeUnscaled = (25, 50)
        self.updateThread = None
        self.animateThread = None
        self.doesAnimate = args['doesAnimate'] if 'doesAnimate' in keys else False
        self.doesUpdate = args['doesUpdate'] if 'doesUpdate' in keys else False
        self.updateInterval = args['updateInterval'] if 'updateInterval' in keys else 30.0
        self.animateInterval = args['animateInterval'] if 'animateInterval' in keys else 30.0
        self.pos = (0,0)
        self.frame_counter_offset = 0
        self.posUnscaled = (0,0)
        self.scene = scene
        self.priority = priority
        self.canvasSize = self.scene.size
        self.group = InstructionGroup()
        self.init = False
        self.__destroy__ = False
        self.__resize__(self.canvasSize[0],self.canvasSize[1])
        self.count = 0
        self.touched = False
        self.scene.resize_event.append(self.__resize__)
        self.scene.on_setActive.append(self.__set_intervals__)
        self.__main_start__()
    
    def __main_start__(self):
        """ Main start function for additional setup after constructor """
        self.__start__()
        self.__pass_start__()
            
    def __start__(self):
        """ *Virtual Function* Override to run functions before object update  """
        pass

    def __pass_start__(self):
        """ End of start set up """
        self.init = True
        self.__set_intervals__(self.scene.isActive())
    
    def __main_update__(self, dt):
        """ Main update function calls virtual update function """
        self.__update__(dt)

    def __update__(self, dt):
        """ *Virtual Function* Override for object logic  """
        print(self, ' is updating without __update__ being overriden')
        pass
    
    def __on_collision__(self, obj):
        """ called while colliding with object """
        self.on_collision(obj)
        pass

    def __on_collision_start__(self,obj):
        """ called at the start of collision """
        self.on_collision_start(obj)
        pass

    def __on_collision_end__(self,obj):
        """ called at the end of collision """
        self.on_collision_end(obj)
        pass

    def on_collision_start(self, obj):
        """ *Virtual Function* Override for collision start  """
        pass

    def on_collision_end(self,obj):
        """ *Virtual Function* Override for collision end  """
        pass

    def on_collision(self, obj):
        """ *Virtual Function* Override for while colliding """
        pass

    def __main_animate__(self, dt):
        """ main animation function """
        self.__animate__(dt)
        self.__pass_animate__(dt)
    
    def __pass_animate__(self, dt):
        """ pass animation to render """
        self.frame_counter = (self.frame_counter if self.frame_counter < self.animateInterval + self.frame_counter_offset else -1 ) + 1
        pass

    def on_touch_down(self, touch):
        """ called when clicked down on self """
        if self.collide_point(*touch.pos):
            self.touched = True
            self.on_click_down(touch)
            return True
        self.touched = False
        return super(Actor, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        """ called when clicked up """
        if self.collide_point(*touch.pos):
            self.touched = False
            self.on_click_up(touch, True)
            return True
        self.touched = False
        self.on_click_up(touch, False)
        return super(Actor, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        """ called when moving while clicked on self """
        if self.collide_point(*touch.pos) and self.touched:
            self.on_click_move(touch)
            return True
        return super(Actor, self).on_touch_move(touch)

    def on_click_down(self, click):
        """ *Virtual Function* Override on click down on self  """
        pass

    def on_click_move(self, click):
        """ *Virtual Function* Override on click move on self  """
        pass

    def on_click_up(self, click, bHovered):
        """ *Virtual Function* Override on click down up  """
        pass

    def __animate__(self, dt):
        """ *Virtual Function* Override for animation logic """
        print(self, ' is animating without __animate__ being overriden')
        pass

    def __main_render__(self):
        """ Main render loop calls virtual render function then passes instructions to main canvas """
        if self.init:
            self.group.clear()
            if not self.__destroy__ and self.debug : self.__debug_render__()
            if not self.__destroy__ : self.__render__()
            self.__pass_render__()

    def __debug_render__(self):
        """ *Virtual Function* Override called before __render__ if debug = True  """
        pass

    def __pass_render__(self):
        """ Send drawing instructions to main canvas """
        self.canvas.clear()
        self.canvas.add(self.group)
        pass
              
    def __render__(self):
        """ *Virtual Function* Override to render custom objects to main canvas  """
        pass

    def __set_collision__(self, b):
        """ enable or disable collision """
        if b :
             self.scene.__add_collision__(self)
             self.collision = True
        else :
             self.scene.__remove_collision__(self)
             self.collision = False
        
    def __end__(self):
        """ *Virtual Function* Override to run code before object destruction """
        pass    
   
    def destroy(self):
        """ Called to destroy object """
        self.__destroy__ = True
        if self.updateThread: Clock.unschedule(self.updateThread)
        if self.animateThread: Clock.unschedule(self.animateThread)
        self.scene.resize_event.remove(self.__resize__)
        self.scene.on_setActive.remove(self.__set_intervals__)
        self.__end__()
        self.scene.__remove_widget__(self)
        self.clear_widgets()
        del self.scene

    def __resize__(self, x,y):
        """ Adjust actor size and positions based new canvas resize """
        self.canvasSize = self.scene.size
        self.setPos(self.posUnscaled)
        self.setSize(self.sizeUnscaled)
        self.__on_resize__()

    def __on_resize__(self):
        """ Called when size of self or window changes """
        pass

    def __set_intervals__(self, b):
        """ Pause or Resume update/render loops after being set inactive
        or active

        Attributes:
            b (bool): Set active/inactive
         """
        if not self.init: return
        if not b:
            if self.doesAnimate and self.animateThread:
                Clock.unschedule(self.animateThread)
                self.animateThread = None
            if self.doesUpdate and self.updateThread : 
                Clock.unschedule(self.updateThread)
                self.updateThread = None

        elif b:
            if self.doesAnimate and self.animateThread is None:
                self.animateThread = Clock.schedule_interval(self.__main_animate__, 1/self.animateInterval)
            if self.doesUpdate and self.updateThread is None:
                self.updateThread = Clock.schedule_interval(self.__main_update__, 1.0/self.updateInterval)

    def setPos(self, p):
        """ Set object position
        
            Attributes:
                    p (tuple) : position to set for actor ( size relative to p/100 * window size + camera position )
         """
        self.posUnscaled = p
        self.pos = ( ((p[0]/100)*self.canvasSize[0] + self.scene.cameraPos[0] ) ,(p[1]/100)*self.canvasSize[1]+self.scene.cameraPos[1])
        self.__on_resize__()

    def setPosScaled(self, p):
        """ set object position relative to window """
        self.posUnscaled = ( (  ((100*p[0] - 100*self.scene.cameraPos[0] )/self.canvasSize[0])-self.sizeUnscaled[0]/2
        ,  ((100*p[1] - 100*self.scene.cameraPos[1] )/self.canvasSize[1])-self.sizeUnscaled[1]/2  )  )
        self.setPos(self.posUnscaled)
    
    def getCanvasCenter(self):
        """ Returns tuple of canvas center relative to size """
        return ( 50 - self.sizeUnscaled[0]/2, 50 - self.sizeUnscaled[1]/2  )

    def setSize(self, p):
        """ Set object size 
        
            Attributes:
                p (tuple) : size to set for actor
                 ( size relative to p/100 * window size )
        """
        self.sizeUnscaled = p
        self.size = ( (p[0]/100) *self.canvasSize [0], (p[1]/100) *self.canvasSize [1])       
        self.setPos(self.posUnscaled)

    def calcResize(self, p, b=False):
        """ Determine draw size after window rescale """
        _p = ((p[0]/100)*self.canvasSize[0],(p[1]/100)*self.canvasSize [1])
        return _p if not b else min(_p[0],_p[1])


    def calcRepos(self, p):
        """ Determine draw size after window rescale """
        _p = ((p[0]/100)*self.canvasSize[0]+ self.scene.cameraPos[0],(p[1]/100)*self.canvasSize [1]+ self.scene.cameraPos[1])
        return _p

class UI(Actor):
    """ Abstract class for creating UI """
    def __init__(self, scene, priority, args,**kwargs):
        self.widget_draw = PriorityQueue()
        self.ui_widget = {}
        super(UI, self).__init__(scene, priority, args,**kwargs)

    def __on_resize__(self):
        pass
        
    def __main_render__(self):
        if not self.__destroy__ and self.debug : self.__debug_render__()
        if not self.__destroy__: self.__render__()
        self.__pass_render__()

    def __pass_render__(self):
        self.__update_widgets__()
        pass

    def destroy(self):
        super(UI,self).destroy()
        del self.ui_widget
        del self.widget_draw

    def on_touch_down(self, touch):
        return super(UI, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        return super(UI, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        return super(UI, self).on_touch_move(touch)

    def __update_widgets__(self):
        """ update widgets called at the end of each render """
        while not self.widget_draw.empty():
            w = self.widget_draw.get()
            a = type(w.group['class'].__class__.__name__, 
            (w.group['class'],), {})(**w.group['kwargs'])
            self.add_widget(a)
            self.ui_widget[w.group['name']] = a

    def setPos(self, p):
        """ Set object position 

            Attributes:
                p (tuple) : position to set for actor 
                ( size relative to p/100 * window size )
                Always stays in view of camera

        """
        self.posUnscaled = p
        self.pos = ((p[0]/100)*self.canvasSize[0],(p[1]/100)*self.canvasSize[1])
        self.__on_resize__()

    def create_widget(self, name, _type, priority=0, **kwargs):
        """Create widget to render on current scene's canvas

        Atributes:
            name (string): unique identifier
            _type (class): widget type to create

            **kwargs (**kwargs) : optional arguments
        
        """
        k = self.ui_widget.keys()
        if name not in k:
            self.widget_draw.put(GroupInstructionQueue(priority, {'class':_type, 'kwargs': kwargs, 'name': name}))
        else:
            for k,v in kwargs.items():
                setattr(self.ui_widget[name], k, v) if k not in ['on_press'] else None
            del kwargs


class GroupInstructionQueue(object):
    """ Helper class to add Group Instruction to priority queue """
    def __init__(self, priority, group):
        self.priority = priority
        self.group = group

    def __gt__(self, other):
        return True if self.priority < other.priority else False
    def __lt__(self, other):
        return True if self.priority > other.priority else False

