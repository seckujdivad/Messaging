global snake, actions, bindings, snake_root, oneat, running, end, sounds, canvas, window, gameover, playsound
import tkinter as tk
import time, threading, random, winsound

#Snake game - David Juckes

snake_root = tk.Tk()
snake_root.title('Snake')

running = True

class sounds:
    death = [(800, 200), (760, 200), (720, 200), (680, 200), (640, 200), (600, 200), (560, 200), (520, 200), (480, 2000)] #Death sounds
    eat = [(720, 200), (850, 200)] #Eat sounds

class snake: #Snake config
    direction = 'up'
    length = 2
    class head:
        height = 16
        width = 16
        x = width * 10 + (width / 2)
        y = height * 10 + (width / 2)
        location = 'head.gif'
        image = tk.PhotoImage(data='R0lGODlhEAAQAHAAACH5BAEAAPwALAAAAAAQABAAhwAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAAAioADsxE0hwoMGCzDQMIZKByBCFDB0qHGWMyIQeFzNi3KjB2KghE0D2yIBRJEkioppl8HGRgr2X9npQwJihmTENJe3B0/kyIxFjzBj22AmTJ84hozqJfAlPWiqYDXpoYBb0ItFU0nhezHDsY8iiRUlOrSqVJ88bW5sp3XqDqb2WPYhwCjpk5kWcGUHW7ERS49aNE4hQJQKx8EINRBx2aja3WUpmFB1DNhgQADs=')
    class body:
        refs = []
        location = 'block.gif'
        image = tk.PhotoImage(data='R0lGODlhEAAQAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAQABAAAAiWADsxE0hwoMGCzDQMIZKByBCFDB0qHGWMyIQeFzNi3KjB2KghE0D2yIBRJEkioppl8HGRAkaWPVxOyNDMmIaSGUVmJGKMGcONLTn2GDKqk0iXJC8m7aGBmU+NMl8qPfYxZM6oJJs+jQlU58hmRpUChemSCCefQ6LezDkT7FKNb4k4JQKx7kINRBx2ana2WUpmFP0CNhgQADs=')

snake.body.refs = [(snake.head.x, snake.head.y)]

class food: #Food config
    refs = []
    cap = 2
    location = 'food.gif'
    image=tk.PhotoImage(data='R0lGODlhEAAQAHAAACH5BAEAAPwALAAAAAAQABAAhwAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAAAigALNNczUtm72DCKW9moZtmsJs0uxNQ1UQlUFp2V5lg3jQYjaLr6RNOxhy2it7Ck0KdJUtlUGTruxhc5mtIUuGqSJGTMVwYcOQGTmexAjUp0+XMe0RzKhwZs2KBu3VBNoSW1WXqA6mhKhxoEqMB1WiSmVToFOpI52GXLhwY0yTESFutDhzpj2LJsMuLRo2Fd6IUgmetKeR7MeqUQ/yrDstIAA7')

class actions: #Key binding actions
    def up(none):
        global snake
        if not snake.direction == 'down':
            snake.direction = 'up'
    def down(none):
        global snake
        if not snake.direction == 'up':
            snake.direction = 'down'
    def left(none):
        global snake
        if not snake.direction == 'right':
            snake.direction = 'left'
    def right(none):
        global snake
        if not snake.direction == 'left':
            snake.direction = 'right'

class bindings: #Key bindings
    class up:
        key = ['<w>', '<Up>', '<Key-KP_8>']
        function = actions.up
    class down:
        key = ['<s>', '<Down>', '<KP_8>']
        function = actions.down
    class left:
        key = ['<a>', '<Left>', '<KP_4>']
        function = actions.left
    class right:
        key = ['<d>', '<Right>', '<KP_6>']
        function = actions.right

class canvas:
    height = snake.head.height * 20
    width = snake.head.height * 20

class gameover: #Game over config
    text = 'Game Over'
    font = ('Arial', 20)
    colour = 'red'
    reasonfont = ('Arial', 15)
    reasoncolour = 'green'
    x = canvas.width / 2
    y = (canvas.height / 2) - 20
    rx = x
    ry = y + 25

for bound in bindings.up.key: snake_root.bind(sequence=bound, func=bindings.up.function) #Keys bound to window
for bound in bindings.down.key: snake_root.bind(sequence=bound, func=bindings.down.function)
for bound in bindings.left.key: snake_root.bind(sequence=bound, func=bindings.left.function)
for bound in bindings.right.key: snake_root.bind(sequence=bound, func=bindings.right.function)

window = tk.Canvas(snake_root, height=canvas.height, width=canvas.width) #Create game canvas inside window
window.pack()

def playsound(sound): #Play a group of sounds in lists
    for s in sound:
        freq, dura = s
        winsound.Beep(freq, dura)

def end(reason): #End the game
    global running
    print('END: ' + reason)
    running = False
    window.create_text(gameover.x, gameover.y, font=gameover.font, text=gameover.text, fill=gameover.colour)
    window.create_text(gameover.rx, gameover.ry, font=gameover.reasonfont, text=reason, fill=gameover.reasoncolour)
    file = open('sharefile.txt', 'w')
    file.write(str(len(snake.body.refs)))
    file.close()
    playsound(sounds.death)

def graphics(): #Graphics handler
    images = []
    while running:
        images.clear() #Clear image references
        for part in snake.body.refs: #Render snake body
            x, y = part
            images.append(window.create_image(x, y, image=snake.body.image))
        for part in food.refs: #Render food
            x, y = part
            images.append(window.create_image(x, y, image=food.image))
        snakehead = window.create_image(snake.head.x, snake.head.y, image=snake.head.image) #Render snake head
        time.sleep(0.2) #Delay loop
        window.delete(snakehead) #Remove old snake head
        for part in images: #Remove all other image references
            window.delete(part)
    images.clear()
    #Put all the images on the screen for the game over screen
    for part in snake.body.refs:
        x, y = part
        images.append(window.create_image(x, y, image=snake.body.image))
    for part in food.refs:
        x, y = part
        images.append(window.create_image(x, y, image=food.image))
    snakehead = window.create_image(snake.head.x, snake.head.y, image=snake.head.image)

def movement(): #Handler for up/down/left/right changes
    while running:
        snake.body.refs.remove(snake.body.refs[0])
        snake.body.refs.append((snake.head.x, snake.head.y))
        if snake.direction == 'up':
            snake.head.y = snake.head.y - snake.head.height
        elif snake.direction == 'down':
            snake.head.y = snake.head.y + snake.head.height
        elif snake.direction == 'left':
            snake.head.x = snake.head.x - snake.head.height
        elif snake.direction == 'right':
            snake.head.x = snake.head.x + snake.head.height
        time.sleep(0.2)

def dropfood(): #Make sure the correct amount of food is always dropped
    global food
    while running:
        if not len(food.refs) == food.cap:
            food.refs.append(((random.randint(0, canvas.width / snake.head.width) * snake.head.width) + snake.head.width / 2, (random.randint(0, canvas.height / snake.head.height) * snake.head.height) + snake.head.height / 2))
            fx, fy = food.refs[len(food.refs)-1]
            if fx <= 0 or fy <= 0 or fx >= canvas.width or fy >= canvas.height:
                food.refs.remove(food.refs[len(food.refs)-1])
        time.sleep(0.2)

def oneat(fooditem): #When food is hit
    try:
        global food, snake
        food.refs.remove(fooditem)
        snake.body.refs.append((snake.head.x, snake.head.y))
        playsound(sounds.eat)
    except ValueError:
        0 #Do nothing

def scanfood(): #Check if should be eating food
    global food, end
    while running:
        for fooditem in food.refs:
            if fooditem == (snake.head.x, snake.head.y):
                oneat(fooditem)
            for part in snake.body.refs:
                if fooditem == part:
                    oneat(fooditem)
        if snake.head.x <= 0 or snake.head.y <= 0 or snake.head.x >= canvas.width or snake.head.y >= canvas.height:
            end('Touched edge')
        pos = -1
        for part in snake.body.refs:
            pos = pos + 1
            if part == (snake.head.x, snake.head.y) and not pos == len(snake.body.refs)-1:
                end('Touching body')
        time.sleep(0.1) #Goes twice speed to make sure all connections are caught

#Start all threads
graphics_thread = threading.Thread(target=graphics) #Thread to handle shapes being rendered onto the screen
graphics_thread.daemon = True
graphics_thread.start()

movement_thread = threading.Thread(target=movement)
movement_thread.daemon = True
movement_thread.start()

dropfood_thread = threading.Thread(target=dropfood)
dropfood_thread.daemon = True
dropfood_thread.start()

scanfood_thread = threading.Thread(target=scanfood)
scanfood_thread.daemon = True
scanfood_thread.start()

#snake_root.iconphoto(True, food.image)
snake_root.mainloop()
running = False
