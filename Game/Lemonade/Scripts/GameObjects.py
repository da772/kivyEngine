from kivy.graphics import Color, Rectangle, Line, Rotate
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.clock import Clock

from Core.Rendering.render_kivy import Actor
from Core.Rendering.render_kivy import UI


class Beach_Background1(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.beach = Image(source='image/beach.png')
        super(Beach_Background1,self).__init__(scene, priority,**kwargs)

    def __start__(self):
        self.setSize( (100,100) )


    def on_click_down(self, click):
        pass

    def on_click_move(self, click):
        self.scene.setCameraPosScaled(click.pos)

    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.beach.texture,size=self.size,pos=self.pos))
        

class Beach_Clouds_Moving(Actor):
    def __init__(self, scene, priority, **kwargs):
        self.clouds = Image(source='image/cloud.png')
        self.clouds.texture.wrap = 'repeat'
        self._texcoords = self.clouds.texture.tex_coords
        super(Beach_Clouds_Moving,self).__init__(scene, priority, False,True, 0, 30.0,**kwargs)

    def __animate__(self, dt):
        y_incr = Clock.get_boottime() * 0.01
        x_scale = self.size[0] / float(self.size[0])
        y_scale = self.size[1] / float(self.size[1])
        self._texcoords = [y_incr, y_scale, y_incr + x_scale,y_scale,y_incr +x_scale,0,y_incr,0]
        pass

    def __render__(self):
        self.group.add(Color(1,1,1,.85))
        self.group.add(Rectangle(texture=self.clouds.texture,size=self.canvasSize,pos=self.pos,tex_coords=self._texcoords))



class WalkingMan(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.img = Image(source='image/female1.zip',anim_loop=-1,anim_delay=1/30)
        self.sold = False
        self.soldPos = 0
        self.img.texture.flip_horizontal()
        self._texcoords = self.img.texture.tex_coords
        super(WalkingMan,self).__init__(scene,priority, True, True, 30.0, 30.0, **kwargs)
    
    def __start__(self):
        #self.debug = True
        self.__set_collision__(True)
        self.setSize( (15,60) )
        pass

    def __update__(self, dt):
        if not self.touched:
            self.setPos( ( self.posUnscaled[0] - 2  / 3.25, self.posUnscaled[1]) )
            pass
        if self.sold:
            self.soldPos += .25
            if self.soldPos > 20:
                self.sold = False


        pass

    def __animate__(self, dt):
        """ *Virtual Function* Override for object logic  """
        pass

    def on_collision_start(self,obj):
        #print('Collision started with:',obj)
        self.soldPos = 0
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
            self.group.add(Rectangle(source ='image/dollar.png',
            pos=self.calcRepos( (self.posUnscaled[0] + self.sizeUnscaled[0]/2 - 1.25, self.posUnscaled[1]+self.sizeUnscaled[1]-self.sizeUnscaled[1]/8 + self.soldPos)  )
            , size=self.calcResize( ( 3,self.sizeUnscaled[1]/8) ) ) )
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.img.texture,pos=self.pos, size=self.size, tex_coords=self._texcoords))
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
        self.group.add(Color(1,0,0,.5))
        self.group.add(Rectangle(pos=self.pos, size=self.size))


class MainMenu_Logo(UI):
    def __init__(self, scene,priority, **kwargs):
        self.textSize = 0
        super(MainMenu_Logo, self).__init__(scene,priority,**kwargs)

    def __start__(self):
        #self.debug= True
        pass

    def __debug_render__(self):
        self.create_widget( 'Image', Image, 1000,pos=self.pos, size=self.size)

    def __render__(self):
        self.create_widget( 'Lemonade', Label, 0, text='Lemonade Stand', pos=self.pos, size=self.size, 
        text_size=( (self.size[0] - self.calcResize( (.5,.5) )[0], self.size[1] - self.calcResize((.5,.5))[1] ) ) ,
        font_size=self.calcResize( (self.textSize, self.textSize), True), halign="center", valign="middle",on_press=lambda a : print(), color=(0,0,0,1),
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




        
