import gc
from Game.game import Game
from Core.EntryPoint import Engine
from Core.Rendering.Primitives import Scene
from Core.Rendering.Primitives import SceneManager

from Game.Lemonade.Scripts.GameObjects import *

from random import randrange

class LemonadeGame(Game):
    def __init__(self,**kwargs):
        super(LemonadeGame, self).__init__(**kwargs)
        self.initGameVars()
        self.charList = []
        self.spriteCount = 7
        self.spriteLoadedCount = 0
        self.sprites = {}
        self.spritesLoaded = False
        self.title = 'Lemonade'
        self.icon = 'Resources/Lemonade/icon/icon.ico'
        self.maxfps = 0
        self.bDraw = False
        self.act = None
        self.sound = None
        self.sPlaying = False

    def initGameVars(self):
        self.day = 1
        self.money = 5
       
    def ResetGame(self, scene):
        self.ChangeScene(scene, 'MainMenu')
        self.initGameVars()

    def start(self):
        print('Starting...')
        self.sound = SoundLoader.load('Resources/Lemonade/music/main_song.mp3')
        self.sound.volume = .1
        self.sound.loop = True
        self.sound.play()
        self.sPlaying = True
        self.loadSprites()
        self.CreateMainMenu()

    def playSong(self, b):
        if b:
            self.sPlaying = True
            self.sound.play()
        else:
            self.sPlaying = False
            self.sound.stop()


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
        

        #Load Effects
        self.sprites['dollarEffect'] = AsyncImage(source ='Resources/Lemonade/effects/dollar.png',on_load=self.spriteLoaded,anim_delay=-1)

        pass

    def spriteLoaded(self, a):
        self.spriteLoadedCount += 1
        if (self.spriteLoadedCount >= self.spriteCount):
            print('All sprites loaded')
            self.spritesLoaded = True

    def CreateMainMenu(self):
        #Create Scene
        scene = SceneManager.Create('MainMenu', True)
        #Setup keyboard Callback
        scene.setKeyboardPressUpCallback(self.on_key_up)
        scene.setKeyboardPressDownCallback(self.on_key_down)
        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.CreateDayStart()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,30), 'text':'Start','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.playSong(not self.sPlaying)), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,17), 'text':'Mute Sound','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : Engine.instance.stop() ), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,4), 'text':'Quit' ,'button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Create Background
        scene.CreateActor(Beach_Background1,99)
        scene.CreateActor(Beach_Clouds_Moving, 97)
        scene.CreateActor(Beach_Sea_Moving, 98)
        
        stand = scene.CreateActor(LemonadeStand, 96)
        stand.setSize( (35,90) )
        stand.__set_sprite_size__( stand.sizeUnscaled )
        stand.setPos(stand.getCanvasCenter())

        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)

        return scene

    def CreateDayStart(self):
        if not self.spritesLoaded: return
        #Create scene
        scene = SceneManager.Create('DayStart', True) if SceneManager.Get('DayStart') is None else SceneManager.Get('DayStart')
        if not scene.isActive(): SceneManager.SetActive('DayStart')
        #Create Background
        scene.CreateActor(Beach_Background1,99)
        scene.CreateActor(Beach_Clouds_Moving, 97)
        scene.CreateActor(Beach_Sea_Moving, 98)
        #Create Lemonade stand
        stand = scene.CreateActor(LemonadeStand, 97)
        #Set stand collision size
        stand.setSize( (10,60) )
        #Set stand sprite size/position
        stand.__set_sprite_size__( (25,60) )
        stand.__set_sprite_pos__( (8,0) )
        #Set stand collision position
        stand.setPos(stand.getCanvasCenter())
        #Create Title Bar
        scene.CreateActor(TitleBar, -1)

        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.ResetGame(scene)   ), 'textColor':(1,0,0,1),'size':(5,5)
        ,'pos':(100-5,100-5), 'text':'Quit', 'textSize':2.5 } ) 

         #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : scene.Clear()), 'textColor':(1,0,0,1),'size':(5,5)
        ,'pos':(100-10,100-5), 'text':'Clear', 'textSize':2.5 } ) 

        #Create walking characters
        for x in range(len(self.charList)) :
            p = randrange(0,len(self.charList))
            pos = ( randrange(15, 99, 1), randrange(0, 20, 1))
            speed = randrange(1, 2) + randrange(1,100)/100
            act = scene.CreateActor(WalkingMan, pos[1], { 'char':self.charList.pop(p) })
            act.speed = speed
            act.setPos(pos)
            self.act = act
        #Create level bounds
        ac1 = scene.CreateActor(ActorPickUp)
        ac1.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, WalkingMan) else None
        ac1.setPos( (98, 50 - ac1.sizeUnscaled[1]/2 ) )
        ac2 = scene.CreateActor(ActorPickUp)
        ac2.on_collide_func = lambda obj : obj.__change_dir__() if issubclass(obj.__class__, WalkingMan) else None
        ac2.setPos( (0, 0 ) )

        
        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)

    def ChangeScene(self, scene, new):
        scene.Clear()
        SceneManager.SetActive( new )


    def on_key_up(self, a,b,*c):
        pass


    def collect_garbage(self):
        print('Collecting garbage')
        gc.collect()

    def on_key_down(self, a, b,c,d):
        if c == 'y':
            self.collect_garbage(0)
        pass

    def update(self, deltaTime):
        pass

        

    def end(self):
        print('Ending...')
        pass
