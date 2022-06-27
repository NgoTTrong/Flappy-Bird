from tkinter import *
import random
GAME_WIDTH = 500
GAME_HEIGHT = 700
PIPEWIDTH = 60
PIPEHEIGHT = 300
BIRDWIDTH = 60
BIRDHEIGHT = 45
SPEED = 30
SPACE_SIZE = 10
SPACE_PIPE = 200
class Bird:
    def __init__(self):
        self.x = 100
        self.y = 200
        canvas.create_image(self.x, self.y, anchor=NW, image=birdImage,tag = "bird")
class Pipes:
    def __init__(self):
        self.underPipes = [[300,0],[440,0],[580,0],[720,0],[860,0]]
        self.abovePipes = [[300,0],[440,0],[580,0],[720,0],[860,0]]
        self.canvasAbovePipe = []
        self.canvasUnderPipe = []
        for i in range(0,5):
            rand = random.randint(-200,-100)
            self.abovePipes[i][1] = rand
            self.underPipes[i][1] = rand + PIPEHEIGHT + SPACE_PIPE
        for i in range(0, 5):
            above = canvas.create_image(self.abovePipes[i][0], self.abovePipes[i][1], anchor=NW, image=reversePipeImage)
            self.canvasAbovePipe.append(above)
            under = canvas.create_image(self.underPipes[i][0], self.underPipes[i][1], anchor=NW, image=pipeImage)
            self.canvasUnderPipe.append(under)

def frame(bird,pipes):
    global score
    bird.y += SPACE_SIZE*0.5
    canvas.delete("bird")
    canvas.create_image(0, 0, anchor=NW, image=background)
    canvas.create_image(bird.x, bird.y, anchor=NW, image=birdImage, tag="bird")
    for i in range(0, 5):
        pipes.abovePipes[i][0] -= SPACE_SIZE
        pipes.underPipes[i][0] -= SPACE_SIZE
    if (pipes.abovePipes[0][0] <= -PIPEWIDTH):
        score += 1
        del pipes.abovePipes[0]
        del pipes.underPipes[0]
        abovepipe = [0,0]
        abovepipe[0] = pipes.abovePipes[3][0] + 100 + PIPEWIDTH
        abovepipe[1] = random.randint(-200,-100)
        underpipe = [0, 0]
        underpipe[0] = pipes.underPipes[3][0] + 100 + PIPEWIDTH
        underpipe[1] = abovepipe[1] + SPACE_PIPE + PIPEHEIGHT
        pipes.abovePipes.append(abovepipe)
        pipes.underPipes.append(underpipe)
    for i in range(0, 5):
        canvas.delete(pipes.canvasAbovePipe[-1])
        del pipes.canvasAbovePipe[-1]
        canvas.delete(pipes.canvasUnderPipe[-1])
        del pipes.canvasUnderPipe[-1]
    for i in range(0, 5):
        above = canvas.create_image(pipes.abovePipes[i][0], pipes.abovePipes[i][1], anchor=NW, image=reversePipeImage)
        pipes.canvasAbovePipe.append(above)
        under = canvas.create_image(pipes.underPipes[i][0], pipes.underPipes[i][1], anchor=NW, image=pipeImage)
        pipes.canvasUnderPipe.append(under)
    if checkCollision(bird,pipes):
        gameOver();
    else:
        window.after(SPEED, frame, bird, pipes)
        canvas.create_image(0, 580, anchor=NW, image=ground)
def move(bird):
    bird.y -= SPACE_SIZE*7
    canvas.delete("bird")
    canvas.create_image(bird.x, bird.y, anchor=NW, image=birdImage, tag="bird")

def checkCollision(bird,pipes):
    if bird.y + BIRDHEIGHT > 580:
        return True
    for i in range(0,5):
        if (bird.x >= pipes.abovePipes[i][0] and bird.x <= pipes.abovePipes[i][0] + PIPEWIDTH and bird.y >= pipes.abovePipes[i][1] and bird.y <= pipes.abovePipes[i][1] + PIPEHEIGHT):
            return True
        if (bird.x + BIRDWIDTH >= pipes.abovePipes[i][0] and bird.x + BIRDWIDTH <= pipes.abovePipes[i][0] + PIPEWIDTH and bird.y >= pipes.abovePipes[i][1] and bird.y <= pipes.abovePipes[i][1] + PIPEHEIGHT):
            return True
        if (bird.x >= pipes.underPipes[i][0] and bird.x <= pipes.underPipes[i][0] + PIPEWIDTH and bird.y + BIRDHEIGHT >= pipes.underPipes[i][1] and bird.y + BIRDHEIGHT <= pipes.underPipes[i][1] + PIPEHEIGHT):
            return True
        if (bird.x + BIRDWIDTH >= pipes.underPipes[i][0] and bird.x + BIRDWIDTH<= pipes.underPipes[i][0] + PIPEWIDTH and bird.y + BIRDHEIGHT>= pipes.underPipes[i][1] and bird.y +BIRDHEIGHT<= pipes.underPipes[i][1] + PIPEHEIGHT):
            return True
    return False
def gameOver():
    global score
    global label1
    global label2
    canvas.delete('all')
    canvas.create_image(-350,0,anchor=NW,image=over)
    label1 = Label(window,text="Score : {}".format(score),font=('consolas',40),relief=RAISED)
    label1.place(x=120,y=500)
    label2 = Label(window, text="Press Enter to try again".format(score), font=('consolas', 20), relief=RAISED)
    label2.place(x=70, y=600)
    score = 0
    window.unbind('<space>')
    window.bind('<Return>',lambda event: run())
def run():
    global label
    global first
    canvas.delete('all')
    if first == True:
        first = False
    else:
        label1.destroy()
        label2.destroy()
    bird = Bird()
    pipes = Pipes()
    window.bind('<space>', lambda event: move(bird))
    frame(bird, pipes)
def start():
    canvas.create_image(15, 0, anchor=NW, image=startImage)
def motion(event):
    x, y = event.x, event.y
    if (x < 220 and x > 60 and y > 500 and y < 575):
        run()

window = Tk()
window.bind('<Button-1>', motion)
window.title("Flappy Bird")
window.resizable(False,False)
canvas = Canvas(window, width = GAME_WIDTH,height = GAME_HEIGHT,bg="Black")
canvas.pack()
birdImage = PhotoImage(file='Bird.png')
pipeImage = PhotoImage(file='Pipe.png')
reversePipeImage = PhotoImage(file='ReversePipe.png')
background = PhotoImage(file='Background.png')
over = PhotoImage(file='gameover.png')
ground = PhotoImage(file='Ground.png')
startImage = PhotoImage(file='startScreen.png')
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int(screenWidth/2 - GAME_WIDTH/2)
y = int(screenHeight/2 - GAME_HEIGHT/2)

window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}")
score = 0
label1 = 0
label2 = 0
first = True
start()
window.mainloop()