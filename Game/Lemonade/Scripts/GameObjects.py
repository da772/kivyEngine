from Core.Rendering.Primitives import *
from Game.game import Game
from Core.Rendering.Primitives import Scene
from Core.Rendering.Primitives import SceneManager
from random import randrange

class Background(Actor):
    """ Generic Background Actor
    """
    def __init__(self, scene,priority,args, **kwargs):
        self.back = Image(source=args['background']) if 'background' in args.keys() else  Image()
        super(Background,self).__init__(scene, priority,args,**kwargs)

    def __start__(self):
        self.setSize( (100,100) )
        self.setPos( (0,0) )

    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.back.texture,size=self.size,pos=self.pos))
        
class Beach_Clouds_Moving(Actor):
    """ Beach Moving Clouds Actor
    """
    def __init__(self, scene, priority, args,**kwargs):
        self.clouds = Image(source='Resources/Lemonade/main_menu/cloud1.png')
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
    """ Beach Moving Sea Actor
    """
    def __init__(self, scene, priority, args,**kwargs):
        self.clouds = Image(source='Resources/Lemonade/main_menu/sea1.png')
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


class ShopBackground(Actor):
    """ Item shop background Actor
    """
    def __init__(self, scene, priority, args, **kwargs):
        self.img = Image(source='Resources/Lemonade/objects/shop-background.png')
        super(ShopBackground, self).__init__(scene,priority,args,**kwargs)
        self.setSize( (50,80 ) )
        self.setPos( (5, 10) )

    def __render__(self):
        self.group.add(Color(.5,.8,1,.85))
        self.group.add(Rectangle(texture=self.img.texture,size=self.size,
        pos=self.pos))

class ShopInfoBackground(Actor):
    """" Item Shop Info Background Actor 
    """
    def __init__(self, scene, priority, args, **kwargs):
        self.img = Image(source='Resources/Lemonade/objects/shop-background.png')
        super(ShopInfoBackground, self).__init__(scene,priority,args,**kwargs)
        if 'pos' in args: self.setPos(args['pos'])
        if 'size' in args: self.setSize(args['size'])

    def __render__(self):
        self.group.add(Color(.5,.8,1,.85))
        self.group.add(Rectangle(texture=self.img.texture,size=self.size,
        pos=self.pos))


class LemonadeStand(Actor):
    """ Lemonade Stand Actor
    """
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

class StandingChar(Actor):
    def __init__(self, scene,priority, args, **kwargs):
        super(StandingChar, self).__init__(scene,priority, {'doesAnimate':True, 'animateInterval':30}, **kwargs)
        self.img = Game.instance.sprites['man1']
        self.debug = args['debug'] if 'debug' in args.keys() else False
        self._texcoords = self.img.texture.tex_coords 
        self._texture = self.img.GetFrames()[0]  if self.img else None
        self.__change_dir__()
        self.frame_counter_offset = 1
        self.sizeX = 15
        self.sizeY = 60
        if 'pos' in args: self.setPos(args['pos'])
        if 'size' in args: self.setSize(args['size'])
        self.setSize(  ( float(abs(self.posUnscaled[1]-100)) /100 * self.sizeX, float(abs(self.posUnscaled[1]-100) )/100 * self.sizeY     )  ) 

    def __change_dir__(self):
        if self._texcoords is not None:
            self._texcoords = [ 0 if self._texcoords[0] > 0 else 1, self._texcoords[1], 0 if self._texcoords[2] > 0 else 1,
            self._texcoords[3], 0 if self._texcoords[4] > 0 else 1, self._texcoords[5], 0 if self._texcoords[6] > 0 else 1,
            self._texcoords[7]]

    def __animate__(self,dt):
        self._texture = self.img.GetFrames()[self.frame_counter]  if self.img else None

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(pos=self.pos,size=self.size))

    def __render__(self):
        """ *Virtual Function* Override to render custom objects to main canvas  """
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self._texture,pos= self.pos, size=self.size, tex_coords=self._texcoords))
        pass

class WalkingChar(Actor):
    """ Walking Sprite Actor 
    """
    alive = 0
    def __init__(self, scene,priority, args, **kwargs):
        super(WalkingChar,self).__init__(scene,priority, {'doesAnimate':True, 'doesUpdate':True, 'updateInterval':30,'animateInterval':30}, **kwargs)
        WalkingChar.alive += 1
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

    @staticmethod
    def CalculateChance():
        chance = 0
        base_price = Game.instance.lemon_price+Game.instance.sugar_price+Game.instance.cup_price+Game.instance.ice_price
        prce = Game.instance.sell_price
        weather = Game.instance.weather
        chance += base_price/(prce) if prce < (base_price*2.5) else base_price / (prce*1.75) if prce < (base_price*3.5) else base_price / (prce*2.5)
        chance += (weather/100)/3
        return chance if chance <= 1 else 1.0

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
        if self.img:
            self.setPos( ( self.posUnscaled[0] + self.speed  / 3.25 , self.posUnscaled[1]) )
            pass
        if self.sold:
            self.soldPos += .25
            if self.soldPos > 20:
                self.sold = False
        self.setSize(  ( float(abs(self.posUnscaled[1]-100)) /100 * self.sizeX, float(abs(self.posUnscaled[1]-100) )/100 * self.sizeY     )  ) 
        pass
        
    def __change_dir__(self):
        if self._texcoords is not None:
            self._texcoords = [ 0 if self._texcoords[0] > 0 else 1, self._texcoords[1], 0 if self._texcoords[2] > 0 else 1,
            self._texcoords[3], 0 if self._texcoords[4] > 0 else 1, self._texcoords[5], 0 if self._texcoords[6] > 0 else 1,
            self._texcoords[7]]
            self.speed = -self.speed

    def __end__(self):
        WalkingChar.alive += -1
        if self.char is not None and self.char not in Game.instance.charList:
            Game.instance.charList.append(self.char)

    def __animate__(self, dt):
        """ *Virtual Function* Override for object logic  """
        self._texture = self.img.GetFrames()[self.frame_counter]  if self.img else None
        pass

    def on_collision_start(self,obj):
        if issubclass(obj.__class__, LemonadeStand):
            if Game.instance.lemons > 0 and Game.instance.ice_cubes > 0 and Game.instance.sugar > 0 and Game.instance.cups > 0:
                chance = WalkingChar.CalculateChance()
                #BUY LOGIC
                if randrange(0,100) <= chance*100:
                    Game.instance.lemons -= 1
                    Game.instance.ice_cubes -= 1
                    Game.instance.sugar -= 1
                    Game.instance.cups -= 1
                    Game.instance.money += Game.instance.sell_price
                    Game.instance.daily_earnings += Game.instance.sell_price
                    Game.instance.daily_cups += 1
                    self.soldPos = 0
                    if self.img:
                        tmp = self.img
                        self.img = self.img1
                        self.img1 = tmp
                    self.sold = True
        pass

    def __debug_render__(self):
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(pos=self.pos,size=self.size))
        pass

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
    """ Actor Pickup Actor
    """
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
        self.group.add(Color(1,0,0,1))
        self.group.add(Rectangle(pos=self.pos, size=self.size))

class TitleBar(Actor):
    """ Title Bar Actor
    """
    def __init__(self, scene,priority, args, **kwargs):
        super(TitleBar, self).__init__(scene,priority,args, **kwargs)
    def __start__(self):
        self.setSize( (100, 5 ) )
        self.setPos( ((0,100-5)) )
    def __render__(self):
        self.group.add(Color(.5,.5,.5,.5))
        self.group.add(Rectangle(pos= self.pos, size=self.size))

class FPS_Counter(UI):
    """ FPS_Counter UI
    """
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


class GameText(UI):
    """ Generic Text UI
    """
    def __init__(self, scene, priority, args, **kwargs):
        self.img = args['image'] if 'image' in args else None
        self.imagePos = args['imagePos'] if 'imagePos' in args else (0,0)
        self.imgSize = args['imageSize'] if 'imageSize' in args else (5,5)
        self.textSize = args['textSize'] if 'textSize' in args else 4.5
        self.text = args['text'] if 'text' in args else 'Text'
        self.textFormat = args['textFormat'] if 'textFormat' in args else '{}'
        self.textColor = args['textColor'] if 'textColor' in args else (1,0,0,1)
        self.font = args['font'] if 'font' in args else 'font/Lemonade.otf'
        self.hAlign = args['hAlign'] if 'hAlign' in args else 'center'
        self.valign = args['valign'] if 'valign' in args else 'middle'
        super(GameText, self).__init__(scene,priority, args,**kwargs)
        self.debug = args['debug'] if 'debug' in args else False
        if 'pos' in args: self.setPos(args['pos'])
        if 'size' in args: self.setSize(args['size'])

    def __debug_render__(self):
        self.create_widget('{}debug'.format((str(id(self)))), Button,size=self.size, pos=self.pos  )

    def __render__(self):
        if self.img: 
            self.create_widget( '{}img'.format(str(id(self))) , Image, source=self.img, pos=self.calcRepos(self.imagePos), size=self.calcResize(self.imgSize))

        frmt = []
        for x in self.text: frmt.append(getattr(Game.instance, x,'ERR'))
        fmrt = tuple(frmt)
        self.create_widget( str(id(self)) , Label, text=self.textFormat.format(*frmt), pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True),halign=self.hAlign, valign=self.valign,markup=True,
        color=self.textColor,font_name=self.font)
        pass

class mButton(UI):
    """Generic Button UI
    """
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
    




        
