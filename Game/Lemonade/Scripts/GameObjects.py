from Core.Rendering.Primitives import *
from Game.game import Game
import numpy as np

class Beach_Background1(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.beach = Image(source='Resources/Lemonade/main_menu/beach1.png')#Game.instance.sprites['beach1']
        super(Beach_Background1,self).__init__(scene, priority,**kwargs)

    def __start__(self):
        self.setSize( (100,100) )
        self.setPos( (0,0) )

    def on_click_down(self, click):
        pass

    def on_click_move(self, click):
        self.scene.setCameraPosScaled(click.pos)

    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.beach.texture,size=self.size,pos=self.pos))
        

class Beach_Clouds_Moving(Actor):
    def __init__(self, scene, priority, **kwargs):
        self.clouds = Image(source='Resources/Lemonade/main_menu/cloud1.png')#Game.instance.sprites['cloud1']
        self.clouds.texture.wrap = 'repeat'
        self._texcoords = self.clouds.texture.tex_coords
        super(Beach_Clouds_Moving,self).__init__(scene, priority, False,True, 0, 30.0,**kwargs)

    def __start__(self):
        self.setPos( (0,100-45) )
        self.setSize( (100,45) )
        pass

    def __animate__(self, dt):
        y_incr = Clock.get_boottime() * 0.01
        x_scale = self.size[0] / float(self.size[0])
        y_scale = self.size[1] / float(self.size[1])
        self._texcoords = [y_incr, y_scale, y_incr + x_scale,y_scale,y_incr +x_scale,0,y_incr,0]
        pass

    def __render__(self):
        self.group.add(Color(1,1,1,.85))
        self.group.add(Rectangle(texture=self.clouds.texture,size=self.size,pos=self.pos,tex_coords=self._texcoords))


class LemonadeStand(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.img = Image(source='Resources/Lemonade/objects/lemonade_stand1.png')
        super(LemonadeStand, self).__init__(scene,priority, True, False, 30, 0, **kwargs )
    def __start__(self):
        self.debug = False
        self.setSize( (10,60 ) )
        self.setPos( (48, 25) )
        self.__set_collision__(True)

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(size=self.size,pos=self.pos))

    def __update__(self,dt):
        pass
    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.img.texture,size=self.calcResize( (25,60) ),pos=self.calcRepos( (40,25) )))

class WalkingMan(Actor):
    def __init__(self, scene,priority, **kwargs):
        super(WalkingMan,self).__init__(scene,priority, True, True, 30.0, 30.0, **kwargs)
        self.img = None 
        self.img1 = None
        self._texture = None
        self._texcoords = None
        self.sold = False
        self.soldPos = 0
        self.speed = 1.5
        self.sizeX = 15
        self.sizeY = 60
        self.char = None
        self.frame_counter_offset = 1
    
    def __start__(self):
        self.debug = False
        self.__set_collision__(True)
        self.setPos( (75,0) )
        self.setSize( (15,60) )
        pass

    def SetChar(self, c):
        self.char = c
        self.img = Game.instance.sprites[c]
        self.img1 = Game.instance.sprites["{}cup".format(c)]
        self._texcoords = self.img.texture.tex_coords
        print(Game.instance.charList)

    def __update__(self, dt):
        if not self.touched and self.img:
            self.setPos( ( self.posUnscaled[0] + self.speed  / 3.25 , self.posUnscaled[1]) )
            pass
        if self.sold:
            self.soldPos += .25
            if self.soldPos > 20:
                self.sold = False
        self.setSize(  ( float(np.abs(self.posUnscaled[1]-100)) /100 * self.sizeX, float(np.abs(self.posUnscaled[1]-100) )/100 * self.sizeY     )  ) 
        pass
        
    def __change_dir__(self):
        if self._texcoords is not None:
            self._texcoords = [ 0 if self._texcoords[0] > 0 else 1, self._texcoords[1], 0 if self._texcoords[2] > 0 else 1,
            self._texcoords[3], 0 if self._texcoords[4] > 0 else 1, self._texcoords[5], 0 if self._texcoords[6] > 0 else 1,
            self._texcoords[7]]
            self.speed = -self.speed


    def __destroy__(self):
        if self.char is not None and self.char not in Game.instance.sprites[c]:
            Game.instance.charList.append(self.char)

    def __animate__(self, dt):
        """ *Virtual Function* Override for object logic  """
        self._texture = self.img.GetFrames()[self.frame_counter]  if self.img else None
        pass

    def on_collision_start(self,obj):
        #print('Collision started with:',obj)
        if issubclass(obj.__class__, LemonadeStand):
            self.soldPos = 0
            if self.img:
                tmp = self.img
                self.img = self.img1
                self.img1 = tmp
            self.sold = True
        pass
        
    def on_collision_end(self,obj):
        #print('Collision ended with:', obj)
        pass

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(pos=self.pos,size=self.size))
        pass

    def on_collision(self, obj):
        #print (obj)
        pass

    def on_click_move(self, click):
        self.setPosScaled(click.pos)

    def __render__(self):
        """ *Virtual Function* Override to render custom objects to main canvas  """
        if self.sold:
            self.group.add(Color(0,1,0,1))
            self.group.add(Rectangle(texture=Game.instance.sprites['dollarEffect'].texture,
            pos=self.calcRepos( (self.posUnscaled[0] + self.sizeUnscaled[0]/2 - 1.25, self.posUnscaled[1]+self.sizeUnscaled[1]-self.sizeUnscaled[1]/8 + self.soldPos)  )
            , size=self.calcResize( ( 3,self.sizeUnscaled[1]/8) ) ) )
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self._texture,pos= self.pos, size=self.size, tex_coords=self._texcoords))
        pass

class ActorPickUp(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.on_collide_func = None
        super(ActorPickUp, self).__init__(scene,priority,**kwargs)
    
    def __start__(self):
        self.setSize( (5, 100))
        self.__set_collision__(True)

    def __on_collision_start__(self, obj):
        if self.on_collide_func : self.on_collide_func(obj)
        pass
            
    def __render__(self):
        self.group.add(Color(1,0,0,0))
        self.group.add(Rectangle(pos=self.pos, size=self.size))


class TitleBar(Actor):
    def __init__(self, scene,priority, **kwargs):
        super(TitleBar, self).__init__(scene,priority, **kwargs)
    def __start__(self):
        self.setSize( (100, 5 ) )
        self.setPos( ((0,100-5)) )
    def __render__(self):
        self.group.add(Color(.5,.5,.5,.5))
        self.group.add(Rectangle(pos= self.pos, size=self.size))


class FPS_Counter(UI):
    def __init__(self, scene, priority, **kwargs):
        super(FPS_Counter, self).__init__(scene, priority, **kwargs)

    def __start__(self):
        self.debug = False
        self.textSize = 2.5
        self.setSize( (8,5) )
        self.setPos( (100-8, 0) )
        pass

    def __render__(self):
        self.create_widget( 'FpsCounter', Label, 1, color=(1,0,0,1), text="{} fps".format(self.scene.fps), pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle",on_press=lambda a : print())
        #self.create_widget('Button22', Button, 99, color=(0,1,0,.5), size = self.size , pos = self.pos )
        
        pass


class MainMenu_Logo(UI):
    def __init__(self, scene,priority, **kwargs):
        self.textSize = 0
        super(MainMenu_Logo, self).__init__(scene,priority,**kwargs)

    def __start__(self):
        self.debug= False
       
        pass

    def __debug_render__(self):
        
        pass

    def __render__(self):
        self.create_widget( 'Lemonade', Label, 0, color=(1,0,0,1), text='Lemonade Stand', pos=self.pos, size=self.size, 
                text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
                font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle",on_press=lambda a : print(),
                font_name='font/Lemonade.otf', 
                )
        pass

class TestButton1(UI):
    def __init__(self, scene,priority, **kwargs):
        self.textSize = 4.5
        super(TestButton1, self).__init__(scene,priority,**kwargs)
        self.__set_collision__(True)

    def __render__(self):
        self.create_widget( 'Image', Image, source='image/sky.png', pos=self.pos, size=self.size)
        self.create_widget( 'Lemonade', Label, text='Lemonade', pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle",on_press=lambda a : print(), color=(1,0,0,1),
        font_name='font/Impacted2.0.ttf'
        )
        pass




        
