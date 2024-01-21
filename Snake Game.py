from tkinter import *
import random 

GAME_WIDTH = 600 #game constant
GAME_HEIGHT = 600 
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#6CBB3C"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake: #create a snake class
    
    def __init__(self): #constuctor 
        self.body_size = BODY_PARTS
        self.coordinates = [] #list of coordinates 
        self.squares = [] #list of square graphics
        
        for i in range(0, BODY_PARTS): #creating a list of coordninates
            self.coordinates.append([0,0]) #append a new list #start a 0,0 so the snake appears in top left corner
    
        for x, y in self.coordinates: 
            square = canvas.create_rectangle (x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake") #create a rectangle 
            self.squares.append(square) 
            
            
class Food: #create a food class
   
    def __init__(self): #constructor
        
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE #food appears in random spot ---- (range) -- 600/50 leaves 12 spots in x to be randon
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE # * Space to turn into 50 pixels 
        
        self.coordinates = [x, y] #coordnites equals a list of x and y's
        
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food") #create a circle (start, finish) - change to red


def next_turn(snake, food): #pass in objects for this function -- call this when game begin
    
    x, y = snake.coordinates[0]  #unpack the head of snake at index of 0
    
    if direction == "up":
        y -= SPACE_SIZE #move one space up
    elif direction == "down":
        y += SPACE_SIZE #move one space down
    elif direction == "left":
        x -= SPACE_SIZE #move one space left
    elif direction == "right":
        x += SPACE_SIZE #move one space right
    
    snake.coordinates.insert(0, (x, y))#update the coordinate of the snake before next turn
         
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) #create new graphic for head of snake 
    
    snake.squares.insert(0, square) #update Snake's list of squares and add a new one
    
    if x == food.coordinates[0] and y == food.coordinates[1]: #if x and y is at food coordinates (overlapping)
        
        global score #if it touches the food object
        
        score += 1 #score go up by one
        
        label.config(text="Score:{}".format(score)) #relabel and display new score
        
        canvas.delete("food") #after the snake object touches food object, use the "food" tag to delete the food object at that coordinate
        
        food = Food() #create a new food object 
        
    else:   #only delete last part of snake if it did not eat a food object 
        
        del snake.coordinates[-1] #delete the back of the snake (negative 1 index)
    
        canvas.delete(snake.squares[-1]) #delete a square on the canva
    
        del snake.squares[-1] #delete a square in snake
    
    if check_collisions(snake):
        game_over() #call the check collision function and if it is True, call the game_over()
        
    else:
        window.after(SPEED, next_turn, snake, food)  #else call the next_turn function 
        

def change_direction(new_direction): #change_direction function with one parameter
    
    global direction #old direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction   #changes old direction to new direaction   
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    
    x, y = snake.coordinates[0] #unpack snake at index = 0
    
    if x < 0 or x >= GAME_WIDTH: #right border 
        return True
    elif y < 0 or y >= GAME_HEIGHT: #right border 
        return True
    
    for body_part in snake.coordinates[1:]: #if body touches snake
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False #no collison
    

def game_over():
    
    canvas.delete(ALL) #delete everything on the canvas
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")  #game over message
    

window = Tk()
window.title("Snake Game")
window.resizable(False, False) #make the window not resizable

score = 0 
direction = 'down' #old direction

label = Label(window, text="Score:{}".format(score), font=('consolas', 40)) #create a score label
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH) #create a canvas
canvas.pack()

window.update() #renders the window

window_width = window.winfo_width() #make window fit with width
window_height = window.winfo_height() #make window fit with height 
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2)) #make it so the screen appears in the middle of the window
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}") #sets the window geometry
 
window.bind('<Left>',lambda event: change_direction('left')) #bind left key
window.bind('<Right>',lambda event: change_direction('right')) #bind right key
window.bind('<Up>',lambda event: change_direction('up')) #bind up key
window.bind('<Down>',lambda event: change_direction('down')) #bind down key

snake = Snake() #create a snake object with constructor 
food = Food() #create a food object with constructor 

next_turn(snake, food)

window.mainloop()