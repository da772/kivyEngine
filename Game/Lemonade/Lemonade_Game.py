from Game.game import Game

from Core.Rendering.Primitives import Scene
from Core.Rendering.Primitives import SceneManager

from Game.Lemonade.Scripts.GameObjects import *

class LemonadeGame(Game):

    def __init__(self,**kwargs):
        super(LemonadeGame, self).__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.title = 'Lemonade'
        self.icon = 'image/icon.ico'
        self.maxfps = 244
        self.bDraw = False
        self.scene1 = None
        self.scene2 = None
       

    def start(self):
        print('Starting...')
        self.scene1 = self.CreateMainMenu()
        self.scene2 = SceneManager.Create('Test', False)

        
    def CreateMainMenu(self):
        scene = SceneManager.Create('MainMenu')
        self.scene1 = scene
        
        scene.setKeyboardPressUpCallback(self.on_key_up)
        scene.setKeyboardPressDownCallback(self.on_key_down)

        #logo = scene.CreateActor(MainMenu_Logo,1)
        #logo.textSize = 10  
        #logo.setSize( (50,25) )
        #logo.setPos( (logo.getCanvasCenter()[0], logo.getCanvasCenter()[1]+25) )

        #vid = scene.CreateActor(TestVideo, -1)

        
        scene.CreateActor(WalkingMan)
        scene.CreateActor(Beach_Background1,99)
        scene.CreateActor(Beach_Clouds_Moving, 98)
        ac1 = scene.CreateActor(ActorPickUp)
        ac1.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, Actor) else None
        ac1.setPos( (98, 50 - ac1.sizeUnscaled[1]/2 ) )

        ac2 = scene.CreateActor(ActorPickUp)
        ac2.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, Actor) else None
        ac2.setPos( (0, 0 ) )

        return scene

    def on_key_up(self, a,b,*c):
        #print(b)
        pass
    def on_key_down(self, a, b,c,d):
        if c[0] == 'y' :
            print( len(self.scene1.widget_list))
        pass


    def update(self, deltaTime):
        self.x += 1

        #self.scene1.setCameraPos( (self.scene1.cameraPosUnscaled[0]+.05, 0) )

        """if (self.x > 150 and self.x < 250):
            if not self.bDraw : SceneManager.SetActive(self.scene2.name)
            self.bDraw = True
        elif self.bDraw is True:
            self.bDraw = False
            SceneManager.Destroy(self.scene2.name, self.scene1.name)"""
        

    def end(self):
        print('Ending...')
        pass
