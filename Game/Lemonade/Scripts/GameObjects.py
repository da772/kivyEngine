from Core.Rendering.Primitives import *
from Game.game import Game
import numpy as np



class Beach_Background1(Actor):
    def __init__(self, scene,priority,args, **kwargs):
        self.beach = Image(source='Resources/Lemonade/main_menu/beach2.png')#Game.instance.sprites['beach1']
        super(Beach_Background1,self).__init__(scene, priority,args,**kwargs)

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
    def __init__(self, scene, priority, args,**kwargs):
        self.clouds = Image(source='Resources/Lemonade/main_menu/cloud1.png')#Game.instance.sprites['cloud1']
        self.clouds.texture.wrap = 'repeat'
        self._texcoords = self.clouds.texture.tex_coords
        super(Beach_Clouds_Moving,self).__init__(scene, priority,{'doesAnimate':True,'animateInterval':30},**kwargs)

    def __start__(self):
        self.setPos( (0,100-35) )
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

class Beach_Sea_Moving(Actor):
    def __init__(self, scene, priority, args,**kwargs):
        self.clouds = Image(source='Resources/Lemonade/main_menu/sea1.png')#Game.instance.sprites['cloud1']
        self.clouds.texture.wrap = 'repeat'
        self._texcoords = self.clouds.texture.tex_coords
        super(Beach_Sea_Moving,self).__init__(scene, priority,{'doesAnimate':True,'animateInterval':30},**kwargs)

    def __start__(self):
        self.setPos( (0,25) )
        self.setSize( (100,45) )
        pass

    def __animate__(self, dt):
        y_incr = Clock.get_boottime() * -0.005
        x_scale = self.size[0] / float(self.size[0])
        y_scale = self.size[1] / float(self.size[1])
        self._texcoords = [y_incr, y_scale, y_incr + x_scale,y_scale,y_incr +x_scale,0,y_incr,0]
        
        pass

    def __render__(self):
        self.group.add(Color(1,1,1,.85))
        self.group.add(Rectangle(texture=self.clouds.texture,size=self.size,pos=self.pos,tex_coords=self._texcoords))


class LemonadeStand(Actor):
    def __init__(self, scene,priority,args, **kwargs):
        self.img = Image(source='Resources/Lemonade/objects/lemonade_stand1.png')
        super(LemonadeStand, self).__init__(scene,priority, args, **kwargs )
        self.setSize( (25,60 ) )
        self.setPos( (25, 25) )
        self.xSize = 0
        self.ySize = 0
        self.xP = ( 0,0)

    def __start__(self):
        self.debug = False
        self.__set_collision__(True)

    def __set_sprite_size__(self, p):
        self.xSize = p[0]
        self.ySize = p[1]

    def __set_sprite_pos__(self,p):
        self.xP = p

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(size=self.size,pos=self.pos))

    def __update__(self,dt):
        pass
    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.img.texture,size=self.calcResize( (self.xSize, self.ySize) ),pos=self.calcRepos( ( self.posUnscaled[0] - self.xP[0],self.posUnscaled[1]-self.xP[1]) )))


class WalkingMan(Actor):
    def __init__(self, scene,priority, args, **kwargs):
        super(WalkingMan,self).__init__(scene,priority, {'doesAnimate':True, 'doesUpdate':True, 'updateInterval':30,'animateInterval':30}, **kwargs)
        self.char = args['char'] if 'char' in args.keys() else None
        self.img = Game.instance.sprites[self.char] if self.char else None 
        self.img1 = Game.instance.sprites["{}cup".format(self.char)] if self.char else None 
        self._texture = self.img.GetFrames()[0]  if self.img else None
        self._texcoords = self.img.texture.tex_coords
        self.SetChar(self.char)
        self.sizeX = 15
        self.sizeY = 60
        self.setPos( (0,0) )
        self.setSize( (0,0) )
        self.sold = False
        self.soldPos = 0
        self.speed = 1.5
        self.frame_counter_offset = 1

    def __start__(self):
        self.debug = False
        self.__set_collision__(True)
        pass

    def SetChar(self, c):
        self.char = c
        self.img = Game.instance.sprites[c]
        self.img1 = Game.instance.sprites["{}cup".format(c)]
        self._texcoords = self.img.texture.tex_coords

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


    def __end__(self):
        if self.char is not None and self.char not in Game.instance.charList:
            Game.instance.charList.append(self.char)

    def __animate__(self, dt):
        """ *Virtual Function* Override for object logic  """
        self._texture = self.img.GetFrames()[self.frame_counter]  if self.img else None
        pass

    def on_collision_start(self,obj):
        if issubclass(obj.__class__, LemonadeStand):
            self.soldPos = 0
            if self.img:
                tmp = self.img
                self.img = self.img1
                self.img1 = tmp
            self.sold = True
        pass
        
    def on_collision_end(self,obj):
        pass

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(pos=self.pos,size=self.size))
        pass

    def on_collision(self, obj):
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
    def __init__(self, scene,priority,args,**kwargs):
        self.on_collide_func = None
        super(ActorPickUp, self).__init__(scene,priority,args,**kwargs)
    
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
    def __init__(self, scene,priority, args, **kwargs):
        super(TitleBar, self).__init__(scene,priority,args, **kwargs)
    def __start__(self):
        self.setSize( (100, 5 ) )
        self.setPos( ((0,100-5)) )
    def __render__(self):
        self.group.add(Color(.5,.5,.5,.5))
        self.group.add(Rectangle(pos= self.pos, size=self.size))

class FPS_Counter(UI):
    def __init__(self, scene, priority,args, **kwargs):
        super(FPS_Counter, self).__init__(scene, priority, args,**kwargs)

    def __start__(self):
        self.debug = False
        self.textSize = 2.5
        self.setSize( (8,5) )
        self.setPos( (100-8, 0) )
        pass

    def __render__(self):
        self.create_widget( 'FpsCounter', Label, 1, color=(1,0,0,1), text="{} fps".format(self.scene.fps), pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle" )
        pass


class MainMenu_Logo(UI):
    def __init__(self, scene,priority, args,**kwargs):
        self.textSize = 0
        super(MainMenu_Logo, self).__init__(scene,priority,args,**kwargs)

    def __start__(self):
        self.debug= False
        pass

    def __debug_render__(self):
        pass

    def __render__(self):
        self.create_widget( 'Lemonade', Label, 0, color=(1,0,0,1), text='Lemonade Stand', pos=self.pos, size=self.size, 
                text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
                font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle",
                font_name='font/Lemonade.otf', 
                )
        pass

class mButton(UI):
    def __init__(self, scene,priority, args,**kwargs):
        self.textSize = args['textSize'] if 'textSize' in args else 4.5
        self.text = args['text'] if 'text' in args else 'Text'
        self.onPress = args['onPress'] if 'onPress' in args else None
        self.textColor = args['textColor'] if 'textColor' in args else (1,0,0,1)
        self.button_normal = args['button_normal'] if 'button_normal' in args else 'atlas://data/images/defaulttheme/button'
        self.button_down = args['button_down'] if 'button_down' in args else 'atlas://data/images/defaulttheme/button_pressed'
        self.font = args['font'] if 'font' in args else 'font/Lemonade.otf'
        self.hAlign = args['hAlign'] if 'hAlign' in args else 'center'
        self.valign = args['valign'] if 'valign' in args else 'middle'
        self.button_img = self.button_normal
        super(mButton, self).__init__(scene,priority,args,**kwargs)
        if 'pos' in args: self.setPos(args['pos'])
        if 'size' in args: self.setSize(args['size'])

    def on_click_down(self, touch):
        self.button_img = self.button_down

    def on_click_up(self, touch, bHovered):
        if bHovered and self.onPress:
            self.onPress()
        self.button_img = self.button_normal

    def __end__(self):
        self.ui_widget[str(id(self))].unbind(on_press=self.OnPressCallback)
        self.ui_widget[str(id(self))].on_press = lambda a=0: None

    def __render__(self):
        self.create_widget( str(id(self)) , Button, text=self.text, pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True), background_normal=self.button_img,
          halign=self.hAlign, valign=self.valign,on_press=self.OnPressCallback, color=self.textColor,
        font_name=self.font)
        pass

    def OnPressCallback(self, instance=None, value=0):
        if self.onPress:
            self.onPress()
    




        
