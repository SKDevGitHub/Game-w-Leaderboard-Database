import tkinter as tk
from tkinter import Button, Label, Tk, Frame, Radiobutton, OptionMenu, messagebox, simpledialog
from PIL import ImageTk, Image #pip install Pillow
import dungeonCrawler
import server_request_handler as query

class Level_designer():
    def __init__(self, username):

        self.username = username
        self.buttons_placed_flag = False

        self.root = Tk()
        self.root.title("Dungeon Crawler")
        self.root.geometry("850x650")
        self.root.columnconfigure((0,1,2),weight=1)
        self.root.columnconfigure(3, weight=9)
        self.root.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)

        #board
        self.board = Frame(self.root, width=650, height=650, bg="black")
        self.board.grid_propagate(False)
        self.board.grid(column=3, rowspan=11,sticky='e')

        #setting images
        self.actman = ImageTk.PhotoImage(Image.open("assets/act-man.png"))
        self.demon = ImageTk.PhotoImage(Image.open("assets/demon.png"))
        self.floor = ImageTk.PhotoImage(Image.open("assets/floor.png"))
        self.ogre = ImageTk.PhotoImage(Image.open("assets/ogre.png"))
        self.wall = ImageTk.PhotoImage(Image.open("assets/wall.png"))

        #setting radio buttons
        self.selected = tk.StringVar()
        self.selected.set("act-man")
        self.ac_pick = Radiobutton(self.root, image=self.actman, variable=self.selected, value="act-man")
        self.ac_pick.grid(row=1,column=2,sticky='e')
        self.de_pick = Radiobutton(self.root, image=self.demon, variable=self.selected, value="demon")
        self.de_pick.grid(row=2,column=2, sticky='e')
        self.fl_pick = Radiobutton(self.root, image=self.floor, variable=self.selected, value="floor")
        self.fl_pick.grid(row=3,column=2,sticky='e')
        self.og_pick = Radiobutton(self.root, image=self.ogre, variable=self.selected, value="ogre")
        self.og_pick.grid(row=4,column=2, sticky='e')
        self.wa_pick = Radiobutton(self.root, image=self.wall, variable=self.selected, value="wall")
        self.wa_pick.grid(row=5,column=2, sticky='e')

        #size menu
        self.height = tk.IntVar()
        self.height.set(8)
        self.height_menu = OptionMenu(self.root, self.height, 3,4,5,6,7,8,9,10,11,12,13,14,15)
        self.height_menu.grid(row=7,column=0, sticky='s')
        self.height_label = Label(self.root, text="Board Height:")
        self.height_label.grid(row=7,column=0,sticky='n')
        
        self.width = tk.IntVar()
        self.width.set(8)
        self.width_menu = OptionMenu(self.root, self.width, 3,4,5,6,7,8,9,10,11,12,13,14,15)
        self.width_menu.grid(row=8,column=0,sticky='s')
        self.width_label = Label(self.root, text='Board Width:')
        self.width_label.grid(row=8,column=0,sticky='n')

        #display board button
        self.display_button = Button(self.root, text="Display")
        self.display_button.bind("<Button-1>", self.populate_board)
        self.display_button.grid(row=9,column=0)

        #submit button TODO: submit to database
        self.submit_button = Button(self.root, text="Submit")
        self.submit_button.bind("<Button-1>", self.submit)
        self.submit_button.grid(row=10,column=2)

        #back button
        self.back_button = Button(self.root, text="<< Back")
        self.back_button.bind("<Button-1>", self.go_back)
        self.back_button.grid(row=0,column=0,sticky='nw')

        self.root.mainloop()

    
    def go_back(self, event):
        self.root.quit()
    
    def populate_board(self, event):
        #remove all buttons
        if(self.buttons_placed_flag):
            for row in self.tiles:
                for tile in row:
                    tile.destroy()

        #calculate the appropriate image size
        #each square can have 600/max(height,width) height and with
        dimension = int(600/max(self.height.get(),self.width.get()))
        dimension = dimension-2

        
        #create empty board and make the edges walls
        self.tilestrings = []
        for i in range(self.height.get()):
            self.tilestrings.append([])
            for j in range(self.width.get()):
                self.tilestrings[i].append("floor")
                if i == 0 or j==0 or j == (self.width.get()-1) or i == (self.height.get()-1):
                    self.tilestrings[i][j] = "wall"
    
        
        #place buttons
        self.ac_button_img = ImageTk.PhotoImage(Image.open("assets/act-man.png").resize((dimension,dimension)))
        self.de_button_img = ImageTk.PhotoImage(Image.open("assets/demon.png").resize((dimension,dimension)))
        self.fl_button_img = ImageTk.PhotoImage(Image.open("assets/floor.png").resize((dimension,dimension)))
        self.og_button_img = ImageTk.PhotoImage(Image.open("assets/ogre.png").resize((dimension,dimension)))
        self.wa_button_img = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((dimension,dimension)))
        self.tiles = []
        for i in range(self.height.get()):
            self.tiles.append([])
            for j in range(self.width.get()):
                if self.tilestrings[i][j] == "wall":
                    self.tiles[i].append(Button(self.board, image=self.wa_button_img,height=dimension,width=dimension))
                elif self.tilestrings[i][j] == "floor":
                    self.tiles[i].append(Button(self.board, image=self.fl_button_img,height=dimension,width=dimension))
                self.tiles[i][j].bind("<Button-1>", lambda event, row=i, col=j: self.change_tile(row,col))
                self.tiles[i][j].grid(row=i,column=j)
        self.buttons_placed_flag = True

    def change_tile(self, j,i):
        new_string = self.selected.get()
        self.tilestrings[j][i] = new_string
        if new_string == "act-man":
            self.tiles[j][i].config(image=self.ac_button_img)
        elif new_string == "demon":
            self.tiles[j][i].config(image=self.de_button_img)
        elif new_string == "floor":
            self.tiles[j][i].config(image=self.fl_button_img)
        elif new_string == "ogre":
            self.tiles[j][i].config(image=self.og_button_img)
        elif new_string == "wall":
            self.tiles[j][i].config(image=self.wa_button_img)



    def submit(self, event):
        #get levelfile string
        self.filestring = ''
        act_man_count = 0
        for row in self.tilestrings:
            for c in row:
                if c == "act-man":
                    self.filestring = self.filestring + 'A'
                    act_man_count = act_man_count+1
                elif c == 'wall':
                    self.filestring = self.filestring + '#'
                elif c == 'demon':
                    self.filestring = self.filestring + 'D'
                elif c == 'floor':
                    self.filestring = self.filestring + ' '
                elif c == 'ogre':
                    self.filestring = self.filestring + 'G'
            self.filestring = self.filestring + '\n'
        
        #check that there is only 1 act man
        if act_man_count != 1:
            messagebox.showerror("Error","You need to have exactly 1 act-man")
            return


        self.gamedata = dungeonCrawler.displayLevel(self.filestring)
        #check that they beat the level
        if self.gamedata[0] == 0:
            messagebox.showerror("Error","You need to beat the game to submit it")
            return
        else:
            #they beat the level, submit it and the solution
            title =  simpledialog.askstring("Level Title","Please name the level:")
            #check that the title is unique
            submitted_level = query.submit_new_level(self.filestring,title,self.username)
            print(submitted_level)
            while not submitted_level:
                title =  simpledialog.askstring("Level Title",f'{title} is taken, please choose a different name:')
                if title == None:
                    break
                submitted_level = query.submit_new_level(self.filestring,title,self.username)
            #submit solution
            query.submit_solution(self.username,title,self.gamedata[1],self.gamedata[0])
            self.root.quit()
            return





if __name__ == "__main__":
    query.connect('localhost',2048)
    z = Level_designer('joe miner')
    query.close_connection()