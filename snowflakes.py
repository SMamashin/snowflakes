import random
from tkinter import *

class Snowflake:
    def __init__(self, canvas, img):
        self.canvas = canvas
        self.size = random.randint(15, 25)
        self.x = random.randint(self.size, 600 - self.size)
        self.y = -self.size
        self.speed = random.randint(7, 10)
        self.img = PhotoImage(file=img).subsample(10)
        self.shape = canvas.create_image(self.x, self.y, anchor=NW, image=self.img)

    def move(self):
        self.y += self.speed
        self.canvas.move(self.shape, 0, self.speed)

class Snowfall:
    def __init__(self, w):
        self.w = w
        self.canvas = Canvas(w, width=600, height=600, bg="#131313")
        self.canvas.pack()
        self.snowflakes = []
        self.collected = 0
        self.basket_img = PhotoImage(file="C:/Users/eva/Desktop/5/source/basket.png").subsample(1)
        # self.basket = self.canvas.create_image(275, 500, anchor=NW, image=self.basket_img) 
        self.counter_text = self.canvas.create_text(250, 10, anchor=NW, text="Собрано: 0", fill="white", font="Arial 14")
        self.you_text = self.canvas.create_text(250, 30, anchor=NW, text="", fill="#03d7fc", font="Arial 16")
        self.basket_width = 100  
        self.basket_height = 100  
        self.basket = self.canvas.create_image(300, 500 - self.basket_height, anchor=NW, image=self.basket_img)

        for _ in range(1):
            self.add_snowflake()

        self.canvas.bind_all('<Key-Left>', self.move_left) 
        self.canvas.bind_all('<Key-Right>', self.move_right)  

    def add_snowflake(self):
        snowflake = Snowflake(self.canvas, "C:/Users/eva/Desktop/5/source/snowflake.png")
        self.snowflakes.append(snowflake)

    def delete_snowflake(self):
        snowflake = Snowflake(self.canvas, "C:/Users/eva/Desktop/5/source/snowflake.png")
        self.snowflakes.clear()

    def animate(self):
        for flake in self.snowflakes[:]:
            flake.move()
            if self.check_collision(flake):
                self.snowflakes.remove(flake)
                self.add_snowflake()
                self.collected += 1 #
                self.canvas.itemconfig(self.counter_text, text=f"Собрано: {self.collected}")
                if self.collected >= 10:
                    self.canvas.itemconfig(self.you_text, text="Круто!")
                    for _ in range(2):
                        self.add_snowflake()
                    if self.collected >= 30:
                        self.canvas.itemconfig(self.you_text, text="Вау!", fill="red")
                        # self.delete_snowflake()
                        for _ in range(3):
                            self.add_snowflake()
                        if self.collected >= 100:
                            self.canvas.itemconfig(self.you_text, text="Ты собрал 100 снежинок!", fill="pink")
                print("+")
        self.w.after(35, self.animate)

    def move_left(self, event):
        x, y = self.canvas.coords(self.basket)
        if x > 0:
            self.canvas.move(self.basket, -20, 0)

    def move_right(self, event):
        x, y = self.canvas.coords(self.basket)
        if x < (600 - self.basket_width):
            self.canvas.move(self.basket, 20, 0)

    def check_collision(self, flake):
        if self.canvas.coords(flake.shape): # снежинка еще на холсте
            flake_coords = self.canvas.coords(flake.shape)
            basket_coords = self.canvas.coords(self.basket)
            basket_x1, basket_y1 = basket_coords[0], basket_coords[1]
            basket_x2, basket_y2 = basket_x1 + self.basket_width, basket_y1 + self.basket_height
            if flake_coords[1] >= basket_y1 and flake_coords[0] >= basket_x1 and flake_coords[0] <= basket_x2:
                self.canvas.delete(flake.shape)
                return True
            elif flake_coords[1] > 600:
                self.add_snowflake() # отрисовка снежинки если чел пропустил
                self.canvas.delete(flake.shape)
                return False  # не собрано
        return False

w = Tk()
w.geometry("600x600")
w.title("Снегопад by Степан")
w.iconbitmap("C:/Users/eva/Desktop/5/source/favicon.ico")
snowfall = Snowfall(w)
snowfall.animate()
w.mainloop()
