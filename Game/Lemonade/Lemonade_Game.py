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
        #Set Game Settings
        self.maxfps = 0
        self.title = 'Lemonade'
        self.icon = 'Resources/Lemonade/icon/icon.ico'
        self.sound = None
        self.sPlaying = False
        #Setup Sprites
        self.charList = []
        self.spriteCount = 7
        self.spriteLoadedCount = 0
        self.sprites = {}
        self.spritesLoaded = False
        #Set Game Vars
        self.initGameVars()
        
    def initGameVars(self):
        self.day = 1
        self.money = 2.50
        self.cups = 0
        self.lemons = 0
        self.ice_cubes = 0
        self.sugar = 0
        self.sell_price = .25
        self.lemon_price = .15
        self.sugar_price = .10
        self.cup_price = .10
        self.ice_price = .05
        self.initCart()

    def initCart(self):
        self.cart_cup = 0
        self.cart_lemon = 0
        self.cart_ice = 0
        self.cart_sugar = 0
        self.cart_total = 0.00


       
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

        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.CreateDayManager()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,30), 'text':'Start','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.playSong(not self.sPlaying)), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,17), 'text':'Mute Sound','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : Engine.instance.stop() ), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,4), 'text':'Quit' ,'button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Create Background
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/main_menu/beach1.png'})
        scene.CreateActor(Beach_Clouds_Moving, 97)
        scene.CreateActor(Beach_Sea_Moving, 98)
        
        stand = scene.CreateActor(LemonadeStand, 96)
        stand.setSize( (35,90) )
        stand.__set_sprite_size__( stand.sizeUnscaled )
        stand.setPos(stand.getCanvasCenter())

        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)
        return scene

    def CreateDayManager(self):
        if not self.spritesLoaded: return
        if SceneManager.Get('DayManager') is None:
            scene = SceneManager.Create('DayManager', True) 
        else:
            SceneManager.SetActive('DayManager')
            return

        scene.setKeyboardPressUpCallback(self.on_key_up)
        scene.setKeyboardPressDownCallback(self.on_key_down)
    
        #Create Titlebar
        self.CreateTitleBar(scene)

        #Create background
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/store_menu/store1.jpg'})

        #Create Shop
        scene.CreateActor(ShopBackground, 1)
        #Title
        scene.CreateActor(GameText, -1, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(37.5,75), 'textFormat':'Item Shop','textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        #Lemons
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(30,65), 'textFormat':'Lemons - ${0:.2f} x {1}', 'text':['lemon_price','cart_lemon'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',-1)), 'textColor':(1,0,0,1),'size':(2,3)
        ,'pos':(54,69), 'text':'-','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',1)), 'textColor':(0,1,0,1),'size':(2,3)
        ,'pos':(57,69), 'text':'+','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Cups
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(30,55), 'textFormat':'Cups - ${0:.2f} x {1}', 'text':['cup_price','cart_cup'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',-1)), 'textColor':(1,0,0,1),'size':(2,3)
        ,'pos':(54,59), 'text':'-','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',1)), 'textColor':(0,1,0,1),'size':(2,3)
        ,'pos':(57,59), 'text':'+','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Ice
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(30,45), 'textFormat':'Ice - ${0:.2f} x {1}', 'text':['ice_price','cart_ice'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',-1)), 'textColor':(1,0,0,1),'size':(2,3)
        ,'pos':(54,49), 'text':'-','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',1)), 'textColor':(0,1,0,1),'size':(2,3)
        ,'pos':(57,49), 'text':'+','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Sugar
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(30,35), 'textFormat':'Sugar - ${0:.2f} x {1}', 'text':['sugar_price','cart_sugar'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',-1)), 'textColor':(1,0,0,1),'size':(2,3)
        ,'pos':(54,39), 'text':'-','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',1)), 'textColor':(0,1,0,1),'size':(2,3)
        ,'pos':(57,39), 'text':'+','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Total
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(35,10), 'hAlign':'center',
        'pos':(32.5,25), 'textFormat':'Total: ${0:.2f}', 'text':['cart_total'],'textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        #Purchase
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.PurchaseCart()), 'textColor':(0,0,0,1),'size':(15,10)
        ,'pos':(42.5,15), 'text':'Purchase!','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.CreateDayStart()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(80,15), 'text':'Start Next Day!','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)

        pass

    def AddToCart(self, item, amt):
        prce = getattr(self, 'cart_{}'.format(str(item)), 0)+amt
        if prce < 0 : return
        setattr(self, 'cart_{}'.format(str(item)), prce)
        self.cart_total += getattr(self, '{}_price'.format(str(item)), 0)*amt
        self.cart_total = abs(self.cart_total)

    def PurchaseCart(self):
        if self.cart_total <= self.money:
            self.money -= self.cart_total
            self.money = abs(self.money)
            self.lemons += self.cart_lemon
            self.ice_cubes += self.cart_ice
            self.sugar += self.cart_sugar
            self.cups += self.cart_cup
            self.initCart()

    def CreateTitleBar(self, scene):
         #Create Title Bar
        scene.CreateActor(TitleBar, -1)
        #Create Title Buttons
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.ResetGame(scene)   ), 'textColor':(1,1,1,1),'size':(5,5)
        ,'pos':(100-5,100-5), 'text':'Quit', 'textSize':2.5 } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.playSong(not self.sPlaying)), 'textColor':(1,1,1,1),'size':(5,5)
        ,'pos':(100-10,100-5), 'text':'Mute', 'textSize':2.5 } ) 
        #Create Info Text
        scene.CreateActor(GameText, -1, {'textColor':(0,1,0,1),'size':(6,5), 'hAlign':'right',
        'pos':(0,100-5), 'textFormat':'${0:.2f}', 'text':['money'], 'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(GameText, -1, {'textColor':(1,1,0,1),'size':(5,5), 'hAlign':'center','image':'Resources/Lemonade/objects/lemon.png',
        'imageSize':(2.5,2.5), 'imagePos':(7,100-3.6),
        'pos':(8,100-5), 'textFormat':'{}', 'text':['lemons'],'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(GameText, -1, {'textColor':(1,0,0,1),'size':(5,5), 'hAlign':'center','image':'Resources/Lemonade/objects/cup.png',
        'imageSize':(2.5,2.5), 'imagePos':(12,100-3.6),
        'pos':(13,100-5), 'textFormat':'{}', 'text':['cups'],'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(GameText, -1, {'textColor':(0,0,1,1),'size':(5,5), 'hAlign':'center','image':'Resources/Lemonade/objects/ice.png',
        'imageSize':(2.5,2.5), 'imagePos':(17,100-3.6),
        'pos':(18,100-5), 'textFormat':'{}', 'text':['ice_cubes'],'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(GameText, -1, {'textColor':(1,1,1,1),'size':(5,5), 'hAlign':'center','image':'Resources/Lemonade/objects/sugar.png',
        'imageSize':(2.5,2.5), 'imagePos':(22,100-3.6),
        'pos':(23,100-5), 'textFormat':'{}', 'text':['sugar'],'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(GameText, -1, {'textColor':(1,1,1,1),'size':(5,5), 'hAlign':'center',
        'pos':(50-5,100-5), 'textFormat':'Day {}', 'text':['day'],'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 

    def SetDayVars(self):
        pass

    def CreateDayStart(self):
        if not self.spritesLoaded: return
        #Create scene
        scene = SceneManager.Create('DayStart', True) if SceneManager.Get('DayStart') is None else SceneManager.Get('DayStart')
        if not scene.isActive(): SceneManager.SetActive('DayStart')
        #Create Background
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/main_menu/beach1.png'})
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
        self.CreateTitleBar(scene)

        #Create walking characters
        for x in range(len(self.charList)) :
            p = randrange(0,len(self.charList))
            pos = ( randrange(15, 99, 1), randrange(0, 20, 1))
            speed = randrange(1, 2) + randrange(1,100)/100
            act = scene.CreateActor(WalkingMan, pos[1], { 'char':self.charList.pop(p) })
            act.speed = speed
            act.setPos(pos)
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
        if scene.name is 'DayStart' : scene.Clear()
        SceneManager.SetActive( new )


    def on_key_up(self, a,b,*c):
        pass


    def collect_garbage(self):
        print('Collecting garbage')
        gc.collect()

    def on_key_down(self, a, b,c,d):
        if c == 'y':
            self.lemons += 1
        pass

    def update(self, deltaTime):
        pass

        

    def end(self):
        print('Ending...')
        pass
