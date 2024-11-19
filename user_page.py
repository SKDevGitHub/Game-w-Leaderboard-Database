from tkinter import Tk, Listbox, Scrollbar, Button, Label
import tkinter as tk
import server_request_handler as query

def displayUser(username):
    class User_page:
        def __init__(self, username):
            self.username = username
            
            self.root = Tk()
            self.root.title("Dungeon Crawler")
            self.root.geometry("800x600")

            self.root.rowconfigure((0,1,2,3,4,5), weight=1)
            self.root.rowconfigure(6, weight=1)
            self.root.columnconfigure((0,1,2,3,4,5,6),weight=1)

            #title
            self.title = Label(self.root, text="User: " + username, font=("TkDefaultFont",16,"bold"))
            self.title.grid(row=0,column=2, sticky='w')
            
            #user's comments
            self.comments = query.get_user_comments(self.username)
            self.comment_label = Label(self.root, text="Comments:")
            self.comment_label.grid(row=5,column=0,sticky='s')
            self.comment_box = Listbox(self.root, selectmode='single')
            self.comment_box.grid(row=6, sticky='nsew',columnspan=7)
            for c in self.comments:
                self.comment_box.insert('end',f'Level: {c[5]}: {c[2]} -> {c[0]} likes, {c[1]} dislikes')
            if self.comments == []:
                self.comment_box.insert('end', 'User has not commented')

            #comments scrollbar
            self.co_scroller = Scrollbar(self.root, orient='vertical', command=self.comment_box.yview)
            self.co_scroller.grid(row=6,column=6, sticky="nse")
            self.comment_box.config(yscrollcommand=self.co_scroller.set)
            self.co_scroll_horiz = Scrollbar(self.root, orient='horizontal', command=self.comment_box.xview)
            self.co_scroll_horiz.grid(row=6,column=0,columnspan=7,sticky='wse')

            #user's completed levels
            self.co_button = Button(self.root, text="Completed Levels")
            self.co_button.bind("<Button-1>", self.show_completed_levels)
            self.co_button.grid(row=2,column=2)

            #user's created levels
            self.cr_button = Button(self.root, text="Created Levels")
            self.cr_button.bind("<Button-1>", self.show_created_levels)
            self.cr_button.grid(row=2,column=1)

            #back button
            self.back_button = Button(self.root, text="<< Back")
            self.back_button.bind("<Button-1>", self.go_back)
            self.back_button.grid(column=0,row=0,sticky="nw")


            self.root.mainloop()
        

        def show_completed_levels(self, event):
            self.completed_screen = Tk()
            self.completed_screen.title(f'{self.username}\'s Completed Levels')
            self.completed_screen.geometry("400x200")
            self.completed_screen.columnconfigure(0,weight=1)

            #listbox
            completed_lvls = query.get_user_completed_levels(self.username)
            self.comp_box = Listbox(self.completed_screen)
            self.comp_box.grid(sticky="nsew",column=0)
            self.comp_scroller = Scrollbar(self.completed_screen, orient="vertical", command=self.comp_box.yview)
            self.comp_scroller.grid(column=0,row=0,sticky="nes")
            for lvl in completed_lvls:
                self.comp_box.insert('end',lvl)
            if completed_lvls == []:
                self.comp_box.insert('end','No levels completed')

        def show_created_levels(self, event):
            self.created_screen = Tk()
            self.created_screen.title(f'{self.username}\'s Created Levels')
            self.created_screen.geometry("400x200")
            self.created_screen.columnconfigure(0,weight=1)

            #listbox
            created_lvls = query.get_user_created_levels(self.username)
            self.cr_box = Listbox(self.created_screen)
            self.cr_box.grid(sticky="nsew",column=0)
            self.cr_scroller = Scrollbar(self.created_screen, orient="vertical", command=self.cr_box.yview)
            self.cr_scroller.grid(column=0,row=0,sticky="nes")
            for lvl in created_lvls:
                self.cr_box.insert('end',lvl)
            if created_lvls == []:
                self.cr_box.insert('end','No levels created')
        
        def go_back(self, event):
            self.root.quit()









if __name__ == "__main__":
    query.connect('localhost',2048)
    displayUser('joe miner')
    query.close_connection()