import math
import json
from os import path
from random import shuffle

from Core.EntryPoint import Engine
from Game.Lemonade.Scripts.GameObjects import *
from Core.Event.EventHandler import WindowEventHandler

class LemonadeGame(Game):
    def __init__(self,**kwargs):
        super(LemonadeGame, self).__init__(**kwargs)
        #Set Game Settings
        self.maxfps = 0
        self.title = 'Lemonade'
        self.icon = 'Resources/Lemonade/icon/leonicon.ico'
        self.WindowSettings()
        Window.size = (self.width,self.height)
        #Setup Window Callbacks
        WindowEventHandler.window_resize_callback.append(self.onResize)
        #Setup Audio
        self.sound = None
        self.sPlaying = False
        #Setup Sprites
        self.charList = []
        self.spriteCount = 10
        self.spriteLoadedCount = 0
        self.sprites = {}
        self.spritesLoaded = False
        self.loadSprites()
        #Set Game Vars
        self.initGameVars()
        
    #Initialize game variables
    def initGameVars(self):
        self.day = 0
        self.dayStart = False
        self.maxDays = 7
        self.starting_money = 100.00
        self.profit = -self.starting_money 
        self.money = self.starting_money
        self.cups = 0
        self.lemons = 0
        self.ice_cubes = 0
        self.sugar = 0
        self.initDay()
        self.initCart()
        self.sell_price = self.lemon_price+self.sugar_price+self.cup_price+self.ice_price
        self.sell_profit = self.sell_price - self.sell_price
        self.sell_chance = WalkingChar.CalculateChance()*100

    #Initialize new day
    def initDay(self):
        self.dayStart = False
        self.day += 1
        self.profit = math.floor((self.money - self.starting_money) * 100)/100.0
        if self.day > self.maxDays:
            self.GameOver(SceneManager.Get('DayStart'))
            return
        shuffle(self.charList)
        self.tickTotal = 60*30
        self.tickCounter = 0
        self.weather = randrange(60,100)
        self.total_people = randrange(90,100) if self.weather < 70 else randrange(130,150) if self.weather < 80 else randrange(200,225) if self.weather < 90 else randrange(250,300)
        self.peoplepertick = math.floor(self.tickTotal/self.total_people)
        self.lemon_price = randrange(10,25)/100
        self.sugar_price = randrange(10,15)/100
        self.cup_price = randrange(10,15)/100
        self.ice_price = randrange(5,10)/100 if self.weather < 80 else randrange(20,45)/100 if self.weather < 90 else randrange(50,75)/100
        self.sell_price = self.lemon_price+self.sugar_price+self.cup_price+self.ice_price
        self.sell_chance = WalkingChar.CalculateChance()*100
        self.daily_earnings = 0.00
        self.daily_cups = 0

    #Initialze shopping cart
    def initCart(self):
        self.cart_cup = 0
        self.cart_lemon = 0
        self.cart_ice = 0
        self.cart_sugar = 0
        self.cart_total = 0.00

    #Reset Game
    def ResetGame(self, scene, b=True):
        self.SaveGame(b)
        self.ChangeScene(scene, 'MainMenu')
        self.initGameVars()

    #Game Over
    def GameOver(self, scene):
        self.ChangeScene(scene, 'GameOver')

    #Continue Game
    def ContinueGame(self):
        bLoaded = False
        try :
            with open('save.json') as settings:
                data = json.load(settings)
                data = data['game']
                self.day = data['day']
                self.money = data['money']
                self.cups = data['cups']
                self.lemons = data['lemons']
                self.ice_cubes = data['ice_cubes']
                self.sugar = data['sugar']
                self.sell_price = data['sell_price']
                bLoaded= True
        except:
            print('Could not load game save.')
        if bLoaded:
            self.initDay()
            self.initCart()
            if not SceneManager.Get('GameOver') or not SceneManager.Get('GameOver').isActive():
                self.CreateDayManager()

    #Game Started
    def start(self):
        print('Starting...')
        self.sound = SoundLoader.load('Resources/Lemonade/music/main_song.mp3')
        self.sound.volume = .1
        self.sound.loop = True
        self.sound.play()
        self.sPlaying = True
        self.CreateMainMenu()

    #Play background music
    def playSong(self, b):
        if b:
            self.sPlaying = True
            self.sound.play()
        else:
            self.sPlaying = False
            self.sound.stop()

    #Load Sprites in background
    def loadSprites(self):

        #Add Characters to array
        self.charList = ['man1', 'man2', 'man3','female1']

        #Load Character Animations
        self.sprites['player'] = AsyncImage(source='Resources/Lemonade/characters/player.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man1'] = AsyncImage(source='Resources/Lemonade/characters/man1.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man1cup'] = AsyncImage(source='Resources/Lemonade/characters/man1cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man2'] = AsyncImage(source='Resources/Lemonade/characters/man2.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man2cup'] = AsyncImage(source='Resources/Lemonade/characters/man2cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man3'] = AsyncImage(source='Resources/Lemonade/characters/man3.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['man3cup'] = AsyncImage(source='Resources/Lemonade/characters/man3cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['female1'] = AsyncImage(source='Resources/Lemonade/characters/female1.zip',on_load=self.spriteLoaded,anim_delay=-1)
        self.sprites['female1cup'] = AsyncImage(source='Resources/Lemonade/characters/female1cup.zip',on_load=self.spriteLoaded,anim_delay=-1)
        
        #Load Effects
        self.sprites['dollarEffect'] = AsyncImage(source ='Resources/Lemonade/effects/dollar.png',on_load=self.spriteLoaded,anim_delay=-1)
        pass

    #Check if all sprites are loaded
    def spriteLoaded(self, a):
        self.spriteLoadedCount += 1
        if (self.spriteLoadedCount >= self.spriteCount):
            print('All sprites loaded')
            self.spritesLoaded = True

    #On Window Resize Event
    def onResize(self, window, w, h):
        self.width = w
        self.height = h
        pass

    #Create the main menu
    def CreateMainMenu(self):
        #Create Scene
        scene = SceneManager.Create('MainMenu', True)
        self.CreateGameOver()
        #Setup keyboard Callback

        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.CreateDayManager()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(35,30), 'text':'Start','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.ContinueGame()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(50,30), 'text':'Continue?','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
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

    #Create Game Over Scene
    def CreateGameOver(self):
        scene = SceneManager.Create('GameOver', False) 
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/main_menu/beach1.png'})
        scene.CreateActor(GameText, -1, {'textColor':(0,0,0,1),'size':(100,10), 'hAlign':'center',
        'pos':(0,60), 'textFormat':'Game Over!','textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(GameText, -1, {'textColor':(0,0,0,1),'size':(100,10), 'hAlign':'center',
        'pos':(0,50), 'textFormat':'You made a profit of: ${0:.2f}', 'text':['profit'],'textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.ResetGame(scene, False)), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(42,30), 'text':'Continue?','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 
        pass

    #Create Day Manager Scene
    def CreateDayManager(self):
        if SceneManager.Get('DayManager') is None:
            scene = SceneManager.Create('DayManager', True) 
        else:
            SceneManager.SetActive('DayManager')
            return
        #Create Titlebar
        self.CreateTitleBar(scene)

        #Create background
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/store_menu/store1.jpg'})

        #Create Shop
        scene.CreateActor(ShopBackground, 1)
        #Title
        scene.CreateActor(GameText, -1, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(17.5,75), 'textFormat':'Item Shop','textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        #Lemons
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(6,65), 'textFormat':'Lemons - ${0:.2f} x {1}', 'text':['lemon_price','cart_lemon'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',-10)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(30,69), 'text':'-10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',-5)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(33.5,69), 'text':'-5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',-1)), 'textColor':(1,0,0,1),'size':(3,3),'textSize':3.5,
        'pos':(37,69), 'text':'-1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',1)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(40.5,69), 'text':'+1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',5)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(44,69), 'text':'+5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('lemon',10)), 'textColor':(0,1,0,1),'size':(3,3),'textSize':3.5,
        'pos':(47.5,69), 'text':'+10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Cups
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(6,55), 'textFormat':'Cups - ${0:.2f} x {1}', 'text':['cup_price','cart_cup'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',-10)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(30,59), 'text':'-10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',-5)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(33.5,59), 'text':'-5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',-1)), 'textColor':(1,0,0,1),'size':(3,3),'textSize':3.5,
        'pos':(37,59), 'text':'-1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',1)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(40.5,59), 'text':'+1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',5)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(44,59), 'text':'+5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('cup',10)), 'textColor':(0,1,0,1),'size':(3,3),'textSize':3.5,
        'pos':(47.5,59), 'text':'+10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Ice
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(6,45), 'textFormat':'Ice - ${0:.2f} x {1}', 'text':['ice_price','cart_ice'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',-10)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(30,49), 'text':'-10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',-5)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(33.5,49), 'text':'-5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',-1)), 'textColor':(1,0,0,1),'size':(3,3),'textSize':3.5,
        'pos':(37,49), 'text':'-1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',1)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(40.5,49), 'text':'+1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',5)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(44,49), 'text':'+5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('ice',10)), 'textColor':(0,1,0,1),'size':(3,3),'textSize':3.5,
        'pos':(47.5,49), 'text':'+10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Sugar
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(25,10), 'hAlign':'center',
        'pos':(6,35), 'textFormat':'Sugar - ${0:.2f} x {1}', 'text':['sugar_price','cart_sugar'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',-10)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(30,39), 'text':'-10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',-5)), 'textColor':(1,0,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(33.5,39), 'text':'-5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',-1)), 'textColor':(1,0,0,1),'size':(3,3),'textSize':3.5,
        'pos':(37,39), 'text':'-1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',1)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(40.5,39), 'text':'+1','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',5)), 'textColor':(0,1,0,1),'size':(3,3), 'textSize':3.5,
        'pos':(44,39), 'text':'+5','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddToCart('sugar',10)), 'textColor':(0,1,0,1),'size':(3,3),'textSize':3.5,
        'pos':(47.5,39), 'text':'+10','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        #Total
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(35,10), 'hAlign':'center',
        'pos':(12.5,25), 'textFormat':'Total: ${0:.2f}', 'text':['cart_total'],'textSize':10 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        #Purchase
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.PurchaseCart()), 'textColor':(0,0,0,1),'size':(15,10)
        ,'pos':(22.5,15), 'text':'Purchase!','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Info Panel
        scene.CreateActor(ShopInfoBackground, 1,{'size':(40,35),'pos':(57,55)})
        #Info Text
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(40,40), 'hAlign':'center', 'valign':'top',
        'pos':(57,49), 'textFormat':'You have 7 days to sell lemonade and make as much money as you can! '
        'To sell lemonade you must have at least 1 lemon, 1 cup, 1 sugar, and 1 ice. There are a couple of factors that determine how well your '
        'lemonade will sell. The first factor is the price at which you are selling your lemonade. The higher the prices the less likely people are to '
        'purchase your lemonade, but sell your lemonade too low and you\'ll run out of money! Another factor that determines how well your lemonade will sell '
        'is the weather. The hotter the weather is the more likely people will be to buy your lemonade, and they will also be willing to pay higher prices too! '
        'The prices of items in the shop differ from day to day, but when it\'s hot the price of ice will skyrocket so buy it when it\'s cheap! '
        , 'text':[],'textSize':2.9 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )

        #Price
        scene.CreateActor(ShopInfoBackground, 1,{'size':(40,39),'pos':(57,11)})
        #Set Price #008000 Green
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(23,10), 'hAlign':'center',
        'pos':(65,40), 'textFormat':'Expected Customers: [color=0000FF]{}[/color]', 'text':['total_people'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(23,10), 'hAlign':'center',
        'pos':(65,35),'textFormat':'Profit per Cup: [color=0000FF]${0:.2f}[/color]', 'text':['sell_profit'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(23,10), 'hAlign':'center',
        'pos':(65,30), 'textFormat':'Chance to Sell: [color=0000FF]%{0:.2f}[/color]', 'text':['sell_chance'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(GameText, 0, {'textColor':(0,0,0,1),'size':(23,10), 'hAlign':'center',
        'pos':(65,24), 'textFormat':'Price:\n[color=0000FF]${0:.2f}[/color]', 'text':['sell_price'],'textSize':5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} )
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddSellPrice(-.01)), 'textColor':(1,0,0,1),'size':(4,4)
        ,'pos':(69.5,28), 'text':'-1c','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddSellPrice(-.05)), 'textColor':(1,0,0,1),'size':(4,4)
        ,'pos':(65.35,28), 'text':'-5c','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddSellPrice(.05)), 'textColor':(0,1,0,1),'size':(4,4)
        ,'pos':(83.75,28), 'text':'+5c','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 
        scene.CreateActor(mButton, -1, {'onPress' : (lambda : self.AddSellPrice(.01)), 'textColor':(0,1,0,1),'size':(4,4)
        ,'pos':(79.5,28), 'text':'+1c','button_normal':'Resources/Lemonade/objects/paper1.png','font':'font/SugarLemonade.ttf' } ) 

        #Create Start Button
        scene.CreateActor(mButton, 0, {'onPress' : (lambda : self.CreateDayStart()), 'textColor':(0,0,0,1),'size':(15,12)
        ,'pos':(69,12), 'text':'Start Day!','button_normal':'Resources/Lemonade/objects/paper1.png' } ) 

        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)
        pass

    #Add Item to cart
    def AddToCart(self, item, amt):
        prce = getattr(self, 'cart_{}'.format(str(item)), 0)+amt
        if prce < 0 :
            setattr(self, 'cart_{}'.format(str(item)), 0)
            self.cart_total -= getattr(self, '{}_price'.format(str(item)), 0)*(abs(amt)-abs(prce))
            self.cart_total = abs(self.cart_total)
            return
        setattr(self, 'cart_{}'.format(str(item)), prce)
        self.cart_total += getattr(self, '{}_price'.format(str(item)), 0)*amt
        self.cart_total = abs(self.cart_total)

    #Increase Sell Price
    def AddSellPrice(self, amt):
        if self.sell_price + amt >= 0:
            self.sell_price += amt
            self.sell_price = abs(self.sell_price)
            self.sell_chance = WalkingChar.CalculateChance()*100
            self.sell_profit = self.sell_price - (self.ice_price+self.cup_price+self.lemon_price+self.sugar_price)


    #Buy Items
    def PurchaseCart(self):
        if math.floor(self.cart_total * 100)/100.0 <= math.floor(self.money * 100)/100.0:
            self.money -= self.cart_total
            self.money = abs(self.money)
            self.lemons += self.cart_lemon
            self.ice_cubes += self.cart_ice
            self.sugar += self.cart_sugar
            self.cups += self.cart_cup
            self.initCart()

    #Create the title bar
    def CreateTitleBar(self, scene, showProfit = False):
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
        scene.CreateActor(GameText, -1, {'textColor':(1,1,1,1),'size':(6,5), 'hAlign':'center',
        'pos':(100-16,100-5), 'textFormat':'{}°F', 'text':['weather'],'textSize':3.5 , 'debug':False, 'font':'font/LucidaSansUnicode.ttf'} ) 

        if showProfit:
            scene.CreateActor(GameText, -1, {'textColor':(1,1,1,1),'size':(15,5), 'hAlign':'center',
            'pos':(100-31,100-5), 'textFormat':'Daily Earings: [color=00FF00]${0:.2f}[/color]', 'text':['daily_earnings'],
            'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 
            scene.CreateActor(GameText, -1, {'textColor':(1,1,1,1),'size':(15,5), 'hAlign':'center',
            'pos':(100-46,100-5), 'textFormat':'Cups Sold Today: [color=00FF00]{}[/color]', 'text':['daily_cups'],
            'textSize':3.5 , 'debug':False, 'font':'font/SugarLemonade.ttf'} ) 

    #Create the day start scene
    def CreateDayStart(self):
        if not self.spritesLoaded: return
        #Create scene
        scene = SceneManager.Create('DayStart', True) if SceneManager.Get('DayStart') is None else SceneManager.Get('DayStart')
        if not scene.isActive(): SceneManager.SetActive('DayStart')
        self.dayStart = True
        self.tickCounter = 0
        #Create Background
        scene.CreateActor(Background,99, {'background':'Resources/Lemonade/main_menu/beach1.png'})
        scene.CreateActor(Beach_Clouds_Moving, 97)
        scene.CreateActor(Beach_Sea_Moving, 98)
        #Create Lemonade stand
        stand = scene.CreateActor(LemonadeStand, 95)
        #Create Player
        player = scene.CreateActor(StandingChar, 96,{'pos':(44,21), 'debug':False})
        #Set stand collision size
        stand.setSize( (10,60) )
        #Set stand sprite size/position
        stand.__set_sprite_size__( (25,60) )
        stand.__set_sprite_pos__( (8,0) )
        #Set stand collision position
        stand.setPos(stand.getCanvasCenter())
         #Create Title Bar
        self.CreateTitleBar(scene, True)

        #Create level bounds
        ac1 = scene.CreateActor(ActorPickUp)
        ac1.on_collide_func = lambda obj : obj.destroy() if issubclass(obj.__class__, WalkingChar) else None
        ac1.setPos( (130, 50 - ac1.sizeUnscaled[1]/2 ) )
        ac2 = scene.CreateActor(ActorPickUp)
        ac2.on_collide_func = lambda obj : obj.destroy() if issubclass(obj.__class__, WalkingChar) else None
        ac2.setPos( (-30, 0 ) )

        #Create FPS Counter
        scene.CreateActor(FPS_Counter, -1)

    #Change current scene
    def ChangeScene(self, scene, new):
        if scene and scene.name is 'DayStart' : scene.Clear()
        SceneManager.SetActive( new )

    #Spawning Characters Logic
    def update(self, deltaTime):
        #If day has started
        if self.dayStart:
            self.tickCounter += 1
            scene = SceneManager.Get('DayStart')
            #If we still have people to spawn and not everyone is destroyed
            if self.total_people <= 0 and WalkingChar.alive <= 0:
                self.dayStart = False
                self.tickCounter = 0
                self.ChangeScene(scene, 'DayManager')
                self.initDay()
                return
            #if we still have people to spawn and it is time to spawn them
            if self.total_people > 0 and self.tickCounter <= self.tickTotal and self.tickCounter % self.peoplepertick is 0:
                self.total_people -= 1
                #print('People: {}, Alive: {}, Tick: {}'.format(self.total_people, WalkingMan.alive, self.tickCounter))
                p = self.total_people % len(self.charList)#randrange(0,len(self.charList))
                _p = randrange(0,2)
                pos = ( -15 if _p is 0 else 115, randrange(0, 20, 1)+self.total_people/1000)
                speed = randrange(1, 2) + randrange(1,100)/100
                act = scene.CreateActor(WalkingChar, pos[1], { 'char':self.charList[p] })
                act.speed = speed
                if _p is 1: act.__change_dir__()
                act.setPos(pos)
        pass

    #Save Game if not over or on main menu
    def SaveGame(self, b=True):
        if b:
            if (SceneManager.Get('MainMenu') is not None and not SceneManager.Get('MainMenu').isActive()) and (SceneManager.Get('GameOver') is not None and not SceneManager.Get('GameOver').isActive()):
                data = {}
                data['game'] = { 'day':self.day if SceneManager.Get('DayStart') is not None and SceneManager.Get('DayStart').isActive() else self.day-1, 
                'money':self.money,'cups':self.cups,'lemons':self.lemons,'ice_cubes':self.ice_cubes,
                'sugar':self.sugar,'sell_price':self.sell_price }
                with open('save.json', 'w') as out:
                    json.dump(data, out)
            else:
                with open('save.json', 'w') as out:
                    json.dump('{}', out)
        else:
            with open('save.json', 'w') as out:
                json.dump('{}', out)
        pass

    #Save Window Size
    def SaveWindowSize(self):
        data = {}
        data['size'] = {'width':self.width,'height':self.height}
        with open('settings.json', 'w') as out:
            json.dump(data, out)
        pass

    #Set Window Size
    def WindowSettings(self):
        w = 1280
        h = 720
        try :
            with open('settings.json') as settings:
                data = json.load(settings)
                w = int(data['size']['width'])
                h = int(data['size']['height'])
        except:
            print('Could not load user settings.')
        self.width = w
        self.height = h

    #Game Over
    def end(self):
        WindowEventHandler.window_resize_callback.remove(self.onResize)
        self.SaveWindowSize()
        self.SaveGame()
        print('Ending...')
        pass
