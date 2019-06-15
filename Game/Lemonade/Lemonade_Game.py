from Game.game import Game

from Core.Rendering.render_kivy import Scene
from Core.Rendering.render_kivy import SceneManager

from Game.Lemonade.Scripts.GameObjects import WalkingMan
from Game.Lemonade.Scripts.GameObjects import Beach_Background1
from Game.Lemonade.Scripts.GameObjects import Beach_Clouds_Moving
from Game.Lemonade.Scripts.GameObjects import MainMenu_Logo


class LemonadeGame(Game):

    def __init__(self,**kwargs):
        super(LemonadeGame, self).__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.title = 'Lemonade'
        self.icon = 'image/icon.ico'
        self.bDraw = False
        self.scene1 = None
        self.scene2 = None

    def start(self):
        print('Starting...')
        self.scene1 = self.CreateMainMenu()
        self.scene2 = SceneManager.Create('Test', False)

        
    def CreateMainMenu(self):
        scene = SceneManager.Create('MainMenu')
        
        scene.setKeyboardPressUpCallback(lambda a, b, *c : print('key up: ', b))
        scene.setKeyboardPressDownCallback(lambda a, b, c, d : print('key down: ', b))

        logo = scene.CreateActor(MainMenu_Logo,1)
        logo.textSize = 10  
        logo.setSize( (40,15) )
        logo.setPos( (logo.getCanvasCenter()[0], logo.getCanvasCenter()[1]+logo.sizeUnscaled[1]+15) )

        #vid = scene.CreateActor(TestVideo, -1)

        
        #scene.CreateActor(WalkingMan)
        scene.CreateActor(Beach_Background1,99)
        scene.CreateActor(Beach_Clouds_Moving, 98)

        return scene


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
