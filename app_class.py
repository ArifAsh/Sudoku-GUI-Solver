import pygame
import sys
from  settings import *



class App():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        self.running = True
        self.mousePos = None
        self.selected = None
        self.shaded = []
        self.Button = None
        self.blankBox = []
        self.font = pygame.font.SysFont("Time New Roman",100,bold=True)
        self.table =table
        self.clear_table = table
        self.num = pygame.font.SysFont("arial",35)
        self.info = pygame.font.SysFont("arial",25)
        
       
    def run(self):

        while self.running:
            self.events()
            self.update()
            self.draw(self.window)
            
            
        pygame.quit()
        sys.exit()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selected = self.mouse_Grid()
                if self.Button:
                    if self.is_clicked(self.Button,self.mousePos):
                        self.table = self.clear_table
                        self.solver(self.table)
                if not self.selected:

                    self.selected = None
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if self.selected != None:
                    num = event.unicode
                    if self.check_input(num) and self.selected not in self.shaded:
                        if self.verify(num,self.selected[1],self.selected[0]):
                            self.table[self.selected[1]][self.selected[0]] = num
                    
    
                    
            
                
    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        
        
    def draw(self,window):
        pygame.display.set_caption("Sudoku")
        window.fill(WHITE)
        if self.selected:
            pass
            self.highlight()
        self.addNum(self.table,window)
        self.drawGrid(window)
        self.drawInfo(window)
        if self.is_full(self.table):
            self.end(window)
    
        pygame.display.update()
        
### HELPER FUNCTION ###

  

    def mouse_Grid(self):
        if self.mousePos[0] < boxpos[0] or self.mousePos[1] < boxpos[1]:
            return False
        if self.mousePos[0]-boxpos[0] > boxSides or self.mousePos[1]-boxpos[1] > boxSides:
            return False
        return [(self.mousePos[0]-boxpos[0])//cellSize,(self.mousePos[1]-boxpos[1])//cellSize]

    def drawGrid(self,window):
        pygame.draw.rect(window,BLACK,(boxpos[0],boxpos[1],boxSides,boxSides),2)
        for lines in range(9):
            if lines % 3 == 0:
                pygame.draw.line(window, BLACK, (boxpos[0]+lines*cellSize, boxpos[1]),(boxpos[0]+lines*cellSize,boxpos[1]+boxSides), 2)
                pygame.draw.line(window, BLACK, (boxpos[0], boxpos[1]+lines*cellSize),(boxpos[0]+boxSides,boxpos[1]+lines*cellSize), 2)
            else:
                pygame.draw.line(window, BLACK, (boxpos[0]+lines*cellSize, boxpos[1]),(boxpos[0]+lines*cellSize,boxpos[1]+boxSides), 1)
                pygame.draw.line(window, BLACK, (boxpos[0], boxpos[1]+lines*cellSize),(boxpos[0]+boxSides,boxpos[1]+lines*cellSize), 1)     
                
    def highlight(self):
        pygame.draw.rect(self.window,BLUE,(boxpos[0]+self.selected[0]*cellSize,boxpos[1]+self.selected[1]*cellSize,cellSize,cellSize))            
        
    def drawInfo(self,window):
        info = self.info.render("Press 0 to clear cell",True,BLACK)
     
        text =self.font.render("SUDOKU",False,WHITE,BLACK) 
        solve = self.info.render("SOLVE",True,WHITE,BLACK)
        text_rect = text.get_rect(center=(WIDTH/2,HEIGHT/2))
        solve_rect = solve.get_rect(center=(WIDTH/2,HEIGHT/2))
        self.Button = solve
        window.blit(text,(text_rect[0],50)) 
        window.blit(info,(infoLine[0],infoLine[1]))
        window.blit(solve,(solve_rect[0],infoLine[1]))
        
        
    def addNum(self,table,window):
        for yidx,rows in enumerate(table):
            for xidx,num in enumerate(rows):
                if num != 0 and type(num) != str and (yidx,xidx) not in self.blankBox:
                    self.shadeBox(window,(xidx,yidx))
                    self.addNumPos(window,num,(xidx,yidx))
                elif num != 0 and int(num) != 0:
                    self.addNumPos(window,int(num),(xidx,yidx))
    def addNumPos(self,window,num,pos):
        pos_x = boxpos[0]+(pos[0]*cellSize)+(cellSize//2)
        pos_y = boxpos[1]+(pos[1]*cellSize)+(cellSize//2)
        
        font = self.num.render(str(num),True,BLACK)
        width =font.get_width()//2
        height = font.get_height()//2
        
        window.blit(font,(pos_x-width,pos_y-height))
        
        
    def shadeBox(self,window,pos):
        pos_x = boxpos[0]+(pos[0]*cellSize)
        pos_y = boxpos[1]+(pos[1]*cellSize)
        self.shaded.append([pos[0],pos[1]])
        pygame.draw.rect(window,GREY,(pos_x,pos_y,cellSize,cellSize))
        
        
    def check_input(self,text): 
        accepted = [str(x) for x in range(10)]   
        if text in accepted:
            return True
        return False
    
    def verify(self,num,x,y):
        if int(num)!= 0:
            # checks row
            for elements in self.table[x]:
                if int(num) == elements or num == elements:
                    return False
            # checks columns
            for elements in range(9):
                if self.table[elements][y] == int(num) or self.table[elements][y] == num:
                    return False   
            #check 3x3 grid
            check_x = x//3
            check_y = y//3
            small_grid = self.table[check_x*3:check_x*3+3]
            for elements in small_grid:
                for char in elements[check_y*3:check_y*3+3]:
                    if int(num) == char or num == char:
                        return False
                                                             
        return True
                
         
    def solver(self,table): 
        if self.find_emptyBox(table):
            y,x = self.find_emptyBox(table)
            if (y,x) not in self.blankBox:
                self.blankBox.append((y,x))
            for n in range(1,10):
                if self.verify(n,y,x):
                    table[y][x] = n 
                    self.draw(self.window)
                    if self.solver(table):
                        return True
                    table[y][x] = 0
        else:
            return True
                
                 
        return False
        
    def is_full(self,table):
        for y in table:
            for x in y:
                if x == 0:
                    return False
        
        return True
         
    def find_emptyBox(self,table):
        for y in range(9):
            for x in range(9):
                if table[y][x] == 0 or type(table[y][x]) == str:
                    return (y,x)
        return None
    
    def is_clicked(self,button,pos):
        but_pos=button.get_size()
       
        but_pos2 = button.get_rect(center=(WIDTH/2,HEIGHT/2))
        if pos[0] < but_pos2[0] or pos[0] > (but_pos[0] + but_pos2[0]):
            return False
        if pos[1] < infoLine[1] or pos[1] > (but_pos[1] + infoLine[1]):
            return False
        return True
    
    def end(self,window):
        font = self.font.render("GAME OVER", False, BLACK,WHITE)
        pos = font.get_size()
        window.blit(font,(WIDTH/2-pos[0]/2,HEIGHT/2-pos[1]/2))
    