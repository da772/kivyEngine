from kivy.graphics import Color, Rectangle, Line
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


    def __render__(self):
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.beach.texture,size=self.canvasSize,pos=self.pos))
        

class Beach_Clouds_Moving(Actor):
    def __init__(self, scene, priority, **kwargs):
        self.clouds = Image(source='image/cloud.png')
        self.clouds.texture.wrap = 'repeat'
        self._texcoords = self.clouds.texture.tex_coords
        super(Beach_Clouds_Moving,self).__init__(scene, priority, False,True, 0, 30.0,**kwargs)

    def __animate__(self, dt):
        y_incr = Clock.get_boottime() * -0.01
        x_scale = self.size[0] / float(self.size[0])
        y_scale = self.size[1] / float(self.size[1])
        self._texcoords = [y_incr, y_scale, y_incr + x_scale,y_scale,y_incr +x_scale,0,y_incr,0]
        pass

    def __render__(self):
        self.group.add(Color(1,1,1,.85))
        self.group.add(Rectangle(texture=self.clouds.texture,size=self.canvasSize,pos=self.pos,tex_coords=self._texcoords))



class WalkingMan(Actor):
    def __init__(self, scene,priority, **kwargs):
        self.img = Image(source='image/spriteSheet.png')
        self.texture = None
        self.map = [ self.img.texture.get_region(0,300,104,149),self.img.texture.get_region(104,300,104,149),
        self.img.texture.get_region(208,300,104,149),self.img.texture.get_region(313,300,104,149),
        self.img.texture.get_region(416,300,104,149),self.img.texture.get_region(520,300,104,149)]
        self.texture = self.map[0]
        super(WalkingMan,self).__init__(scene,priority, True, True, 30.0, 8.0, **kwargs)
    
    def __start__(self):
        self.debug = True
        self.__set_collision__(True)
        self.setSize( (self.sizeUnscaled[0]/2,self.sizeUnscaled[1]))
        pass

    def __update__(self, dt):
        if not self.touched:
            if self.posUnscaled[0] < 95 : self.setPos( ( self.posUnscaled[0] + 4  / 3.25, self.posUnscaled[1]) )
            else : self.setPos( (0, self.posUnscaled[1]) )
        pass

    def __animate__(self, dt):
        """ *Virtual Function* Override for object logic  """
        if self.count < len(self.map):
            self.texture = self.map[self.count]
        else:
            self.count = 0
            self.texture = self.map[self.count]
       
        self.count += 1
        pass

    def on_collision_start(self,obj):
        #print('Collision started with:',obj)
        pass
        
    def on_collision_end(self,obj):
        #print('Collision ended with:', obj)
        pass

    def __debug_render__(self):
        #self.group.add(Color(1,0,0,.5))
        #self.group.add(Rectangle(pos=self.pos,size=self.size))
        pass

    def on_collision(self, obj):
        #print (obj)
        pass


    def on_click_move(self, click):
        self.setPosScaled(click.pos)

    def __render__(self):
        """ *Virtual Function* Override to render custom objects to main canvas  """
        self.group.add(Color(1,1,1,1))
        self.group.add(Rectangle(texture=self.texture,pos=self.pos, size=self.size))
        pass


class MainMenu_Logo(UI):
    def __init__(self, scene,priority, **kwargs):
        self.textSize = 0
        super(MainMenu_Logo, self).__init__(scene,priority,**kwargs)

    def __start__(self):
        self.debug= True
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




        
