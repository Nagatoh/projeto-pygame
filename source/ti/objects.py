import pygame, random
from pygame.locals import*

font = None
font_size = 25
walls = []
obstacles = []
cards_list = []

class GameObject (pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y , width, height, obj_type):
        
        pygame.sprite.Sprite.__init__(self)
        
        
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = pos_y
        self.rect.x = pos_x
        
        self.obj_type = obj_type
        self.acceleration = 0
        self.direction = ""
        
        
class Player (GameObject, pygame.font.Font):
    def __init__(self, image, pos_x, pos_y, width, height, obj_type):
        GameObject.__init__(self,image,pos_x, pos_y ,width,height,0)
        self.image = pygame.image.load('../media/sprites/bob_cima.png')
        self.cash = 0
        self.c_card = 0
        self.time = 180
        self.doce=0
        self.proteina=0
        self.vegetal=0
        self.carbohidrato=0
        self.score=0
        
        self.rect = pygame.Rect (500,300, 30,30)
        pygame.font.Font.__init__(self, font, font_size)
        
        self.walls = walls
        
        self.timeLabel = self.render("Tempo:" + str(self.time), 1, (0,0,0))
        self.cashLabel = self.render("Dinheiro:" + str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render("Cartoes:" + str(self.c_card), 1,(0,0,0))
        self.scoreLabel = self.render("Media Pontos:"+ str(self.score), 1,(0,0,0))
        

        
    def updateScore(self):
        foodSum = (self.doce + self.proteina + self.vegetal + self.carbohidrato)
        self.score = ((self.doce)+(self.proteina)+(self.vegetal)+(self.carbohidrato))/10
        
        
    def buyFood(self,food):
        self.cash -= food.value
        if food.food_type == 'doce':
            self.doce += 3
            if (self.doce >= 10):
                self.doce = 10
        elif food.food_type == 'proteina':
            self.proteina += 5
            if (self.proteina >= 20):
                self.proteina = 20
        elif food.food_type == 'vegetal':
            self.vegetal += 6
            if (self.vegetal >= 30):
                self.vegetal = 30
        elif food.food_type == 'carbohidrato':
            self.carbohidrato += 8
            if (self.carbohidrato >= 40):
                self.carbohidrato = 40
            
        self.updateScore()
        
    def moveUp(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/sprites/bob_cima.png')
        self.rect.top -= self.acceleration
        for wall in block_hit_list:
            if self.rect.top - 10 < wall.rect.bottom:          
                self.rect.top = wall.rect.bottom
            else:
                self.rect.top -= self.acceleration
       
        
    def moveDown(self): 
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        
        self.image = pygame.image.load('../media/sprites/bob_baixo.png')
        self.rect.bottom += self.acceleration
        #print len(block_hit_list)
        for wall in block_hit_list:
            if self.rect.bottom + 10> wall.rect.top:          
                self.rect.bottom = wall.rect.top
            else:    
                self.rect.bottom += self.acceleration          
        
    def moveLeft(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/sprites/bob_esquerda.png')
        self.rect.left -= self.acceleration
        for wall in block_hit_list:
            if self.rect.left - 10 < wall.rect.right:            
                self.rect.left = wall.rect.right              
            else:
                self.rect.left -= self.acceleration
        
    def moveRight(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        self.image = pygame.image.load('../media/sprites/bob_direita.png')
        self.rect.right += self.acceleration
        for wall in block_hit_list:
            if self.rect.right + 10> wall.rect.left:          
                self.rect.right = wall.rect.left
            else:
                self.rect.right += self.acceleration
        
        
    def updateValues(self):
        self.timeLabel = self.render("Tempo:" + str(self.time), 1, (0,0,0))
        self.cashLabel = self.render("Dinheiro:" + str(self.cash), 1, (0,0,0))
        self.c_cardLabel = self.render("Cartoes:" + str(self.c_card), 1, (0,0,0))
        
        score_color = (0,0,0)
        if self.score >= 7:
            score_color = (0,200,0)
        if self.score < 7:
            score_color = (150,180,0)
        if self.score < 5:
            score_color = (180,150,0)
        if self.score < 3:
            score_color = (200,0,0) 
     
        self.scoreLabel = self.render("Media Pontos:"+ str(self.score),1,score_color)
        

class Wall (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x,pos_y,width,height,obj_type)
        if (obj_type == 8):
            self.image = pygame.image.load('../media/sprites/gondula-x.png')
        elif (obj_type == 9):
            self.image = pygame.image.load('../media/sprites/gondula-y.png')
        
        #obstacles.append(self)
        #self.image = pygame.Surface([width,height])
        

        
class Cash (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x ,pos_y , width, height, 2)
        self.image = pygame.image.load('../media/sprites/c_card.png')
        self.rect = pygame.Rect(pos_x, pos_y, 60, 60)
    

class FastFood (GameObject):
    def __init__(self,image,pos_x,pos_y,width,height, obj_type):
        GameObject.__init__(self,image,pos_x,pos_y, width, height, obj_type)
        
        self.image = pygame.image.load('../media/sprites/steve.png')
        self.rect = pygame.Rect (pos_x, pos_y, 32,40)
        self.movingPositive = True
        #self.image = pygame.image.load('../media/bob_cima.png')

class ATM(GameObject):
    def __init__(self,image,pos_x,pos_y,width,height,obj_type):
        GameObject.__init__(self,image,pos_x,pos_y,width,height,2)

        self.image = pygame.image.load('../media/sprites/atm.png')
        self.rect = pygame.Rect(pos_x, pos_y, 37, 60)
        
class Food(GameObject):
    def __init__(self,value,food_type):
        GameObject.__init__(self,"",0,0,0,0,10)
        
        self.value = value
        self.food_type = food_type
        self.prepareSprite()
        
    def prepareSprite(self):
        if (self.food_type == "vegetal"):
            self.prepareVegetable()
        elif (self.food_type == "proteina"):
            self.prepareProtein()
        elif (self.food_type == "carbohidrato"):
            self.prepareCarbo()
        elif (self.food_type == "doce"):
            self.prepareCandy()

    
    def prepareVegetable (self):
        basePath = '../media/sprites/frutasEvegetais/'
        randomImg = random.randint(0,5)
        if (randomImg == 0):
            self.image = pygame.image.load(basePath + 'banana.png')
        elif (randomImg == 1):
            self.image = pygame.image.load(basePath + 'brocolis.png')
        elif (randomImg == 2):
            self.image = pygame.image.load(basePath + 'cenoura.png')
        elif (randomImg == 3):
            self.image = pygame.image.load(basePath + 'ervilha.png')
        elif (randomImg == 4):
            self.image = pygame.image.load(basePath + 'maca.png')
        elif (randomImg == 5):
            self.image = pygame.image.load(basePath + 'tomate.png')
        
        self.rect = pygame.Rect (170, 160, 70,80)
    
    def prepareProtein(self):
        basePath = '../media/sprites/proteinas/'
        randomImg = random.randint(0,3)
        if (randomImg == 0):
            self.image = pygame.image.load(basePath + 'egg.png')
        elif (randomImg == 1):
            self.image = pygame.image.load(basePath + 'espeto.png')
        elif (randomImg == 2):
            self.image = pygame.image.load(basePath + 'meat.png')
        elif (randomImg == 3):
            self.image = pygame.image.load(basePath + 'milk.png')
        
        self.rect = pygame.Rect (670, 150, 70,70)
        
    def prepareCarbo(self):
        basePath = '../media/sprites/carbohidratos/'
        randomImg = random.randint(0,3)
        if (randomImg == 0):
            self.image = pygame.image.load(basePath + 'bread.png')
        elif (randomImg == 1):
            self.image = pygame.image.load(basePath + 'corn.png')
        elif (randomImg == 2):
            self.image = pygame.image.load(basePath + 'rice.png')
        elif (randomImg == 3):
            self.image = pygame.image.load(basePath + 'pasta.png')
        


        self.rect = pygame.Rect (670, 360, 70,80)
    
    def prepareCandy(self):
        basePath = '../media/sprites/docesEgorduras/'
        randomImg = random.randint(0,3)
        if (randomImg == 0):
            self.image = pygame.image.load(basePath + 'cookie.png')
        elif (randomImg == 1):
            self.image = pygame.image.load(basePath + 'donut.png')
        elif (randomImg == 2):
            self.image = pygame.image.load(basePath + 'picole.png')
        elif (randomImg == 3):
            self.image = pygame.image.load(basePath + 'pizza.png')
        
        self.rect = pygame.Rect (170, 350, 70,70)