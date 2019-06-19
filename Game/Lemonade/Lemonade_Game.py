from Game.game import Game

from Core.Rendering.Primitives import Scene
from Core.Rendering.Primitives import SceneManager

from Game.Lemonade.Scripts.GameObjects import *

from random import randrange

class LemonadeGame(Game):

    def __init__(self,**kwargs):
        super(LemonadeGame, self).__init__(**kwargs)
        self.x = 0
        self.charList = []
        self.spriteCount = 10
        self.spriteLoadedCount = 0
        self.sprites = {}
        self.spritesLoaded = False
        self.y = 0
        self.title = 'Lemonade'
        self.icon = 'image/icon.ico'
        self.maxfps = 0
        self.bDraw = False
        self.scene2 = None
        self.act = None
       
    def start(self):
        print('Starting...')
        self.loadSprites()
        self.CreateMainMenu()
        self.scene2 = SceneManager.Create('Test', False)

    def loadSprites(self):

        #Add Characters to array
        self.charList = ['man1', 'man2', 'female1']

        #Load Character Animations
        self.sprites['man1'] = AsyncImage(source='Resources/Lemonade/characters/man1.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man1cup'] = AsyncImage(source='Resources/Lemonade/characters/man1cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man2'] = AsyncImage(source='Resources/Lemonade/characters/man2.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man2cup'] = AsyncImage(source='Resources/Lemonade/characters/man2cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['female1'] = AsyncImage(source='Resources/Lemonade/characters/female1.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['female1cup'] = AsyncImage(source='Resources/Lemonade/characters/female1cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        

        #Load Background
        self.sprites['cloud1'] = AsyncImage(source='Resources/Lemonade/main_menu/cloud1.png',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['beach1'] = AsyncImage(source='Resources/Lemonade/main_menu/beach1.png',on_load=self.spriteLoaded,anim_delay=-1)

        #Load Objects
        self.sprites['lemonade_stand1'] = AsyncImage(source='Resources/Lemonade/objects/lemonade_stand1.png',on_load=self.spriteLoaded,anim_delay=-1)

        #Load Effects
        self.sprites['dollarEffect'] = AsyncImage(source ='Resources/Lemonade/effects/dollar.png',on_load=self.spriteLoaded,anim_delay=-1)

        pass

    def spriteLoaded(self, a):
        self.spriteLoadedCount += 1
        if (self.spriteLoadedCount >= self.spriteCount):
            print('All sprites loaded')
            self.spritesLoaded = True

    def CreateMainMenu(self):
        scene = SceneManager.Create('MainMenu', True)
        self.scene1 = scene
        
        scene.setKeyboardPressUpCallback(self.on_key_up)
        scene.setKeyboardPressDownCallback(self.on_key_down)

        logo = scene.CreateActor(MainMenu_Logo,1)
        logo.textSize = 10  
        logo.setSize( (50,25) )
        logo.setPos( (0,0) )#(logo.getCanvasCenter()[0], logo.getCanvasCenter()[1]+25) )
        scene.CreateActor(FPS_Counter, -1)
        scene.CreateActor(Beach_Background1,99)
        scene.CreateActor(Beach_Clouds_Moving, 98)
        scene.CreateActor(LemonadeStand, 97)
        scene.CreateActor(TitleBar, -1)

        ac1 = scene.CreateActor(ActorPickUp)
        ac1.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, WalkingMan) else None
        ac1.setPos( (98, 50 - ac1.sizeUnscaled[1]/2 ) )

        ac2 = scene.CreateActor(ActorPickUp)
        ac2.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, WalkingMan) else None
        ac2.setPos( (0, 0 ) )

        """
        for x in range(1) :
            pos = ( randrange(15, 99, 1), randrange(0, 25, 1))
            speed = randrange(1, 2) + randrange(1,100)/100
            act = scene.CreateActor(WalkingMan, pos[1])
            act.speed = speed
            act.setPos(pos)
            self.act = act
            pass

        ac1 = scene.CreateActor(ActorPickUp)
        ac1.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, Actor) else None
        ac1.setPos( (98, 50 - ac1.sizeUnscaled[1]/2 ) )

        ac2 = scene.CreateActor(ActorPickUp)
        ac2.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, Actor) else None
        ac2.setPos( (0, 0 ) )"""
        return scene

    def on_key_up(self, a,b,*c):
        #print(b)
        pass
    def on_key_down(self, a, b,c,d):
        if c[0] == 'y' :
            scene = SceneManager.Get('MainMenu')
            for x in range(len(self.charList)) :
                p = randrange(0,len(self.charList))
                pos = ( randrange(15, 99, 1), randrange(0, 25, 1))
                speed = randrange(1, 2) + randrange(1,100)/100
                act = scene.CreateActor(WalkingMan, pos[1])
                act.SetChar(self.charList.pop(p))
                act.speed = speed
                act.setPos(pos)
                self.act = act
                pass
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
