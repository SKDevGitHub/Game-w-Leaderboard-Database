from tkinter import Button, Label, Tk, Scrollbar, Entry, Listbox, OptionMenu
import tkinter as tk
from server_request_handler import ServerRequestHandler
#import dungeonCrawler



def display_level(levelname, username):
    
    def play_game(event):
        #TODO remove and add widgets
        #solution, score = dungeonCrawler.startGame()
        display_rating_section()


    def display_rating_section():
        diff_rating_menu.grid(column=6,row=1,sticky='e')
        rating_menu.grid(column=6,row=1,sticky='w')
        rating_label.grid(column=6,row=1,sticky='n')
        submit_rating_button.grid(column=6, row=2,sticky='n')


    def submit_rating(event):
        #TODO:
        x=1

    def display_leaderboard(event):
        lb = Tk()
        lb.title(levelname)
        lb.geometry("400x200")

        #TODO: query for leaderboard data and put it in listbox w/scrollbar

    def closed_window():
        #TODO: do i need this?
        root.quit()
        return "quit"

    def go_back(event):
        root.quit()

    def add_comment(event):
        text = comment_entry.get()
        comment_entry.delete(0, tk.END)

        #TODO: client.create_comment()

    def like_comment(event):
        index = comment_box.curselection()
        index = index[0]
        #TODO: change this based on what the query returns

        #commentID = comments[index][3]
        #client.like_comment(commentID)

    def dislike_comment(event):
        index = comment_box.curselection()
        index = index[0]
        #TODO: change this based on what the query returns

        #commentID = comments[index][3]
        #client.dislike_comment(commentID)
    
    #query for comments
    #client = ServerRequestHandler
    #comments = client.find_comments(levelname)
    #test value
    comments = [["comment text", 2, 0, 6]]
    comment_amount = len(comments)

    #create gui
    root = Tk()
    root.title("Dungeon Crawler")
    root.geometry('800x600')
    root.rowconfigure((0,1,2), weight=1)
    root.rowconfigure(3, weight=3)
    root.columnconfigure((0,1,2,3,4,5,6),weight=1)
    level_played_flag = False

    #comments section init
    comment_box = Listbox(root, selectmode=tk.SINGLE)
    comment_box.grid(row=3, sticky='nsew',columnspan=7)
    #TODO: change range(50) to comment amount
    for n in range(50):
        #TODO: save the id of each comment
        comment_box.insert(tk.END, f'{comments[0][0]} : {n} likes, {comments[0][2]} dislikes')
    
    scroller = Scrollbar(root, orient=tk.VERTICAL, command=comment_box.yview)
    scroller.grid(row=3,column=6, sticky="nse")
    comment_box.config(yscrollcommand=scroller.set)

    #play level button
    title = Label(root, text="level: " + levelname, font=("TkDefaultFont",16,"bold"))
    play_level_button = Button(root, text="Play " + levelname[:10])
    title.grid(row=0,column=3,sticky='n')
    play_level_button.bind("<Button-1>", play_game)
    play_level_button.grid(row=0,column=4, sticky="n")

    #add a comment
    comment_label = Label(root, text="Enter a comment:")
    comment_entry = Entry(root, text="")
    comment_button = Button(root, text="Add Comment")
    comment_button.bind("<Button-1>", add_comment)
    comment_label.grid(row=2,column=0)
    comment_entry.grid(row=2,column=0,columnspan=3,sticky='wse')
    comment_button.grid(row=2,column=3,sticky='s')


    #like and dislike comments
    like_comment_button = Button(root, text="Like")
    like_comment_button.bind("<Button-1>", like_comment)
    like_comment_button.grid(row=2,column=5, sticky="se")
    dislike_comment_button = Button(root, text="Dislike")
    dislike_comment_button.bind("<Button-1>", dislike_comment)
    dislike_comment_button.grid(row=2,column=6,  sticky="sw")

    #back button
    back_button = Button(root,text="<< Back")
    back_button.bind("<Button-1>", go_back)
    back_button.grid(row=0,column=0,sticky="nw")

    #if the window is closed, end application
    root.protocol("WM_DELETE_WINDOW", closed_window)

    #leaderboard
    leaderboard_button = Button(root,text="View Leaderboard")
    leaderboard_button.bind("<Button-1>", display_leaderboard)
    leaderboard_button.grid(row=1,column=0,sticky='s')

    #amount of users played TODO:query for users played amount
    amount_played = 3
    amount_played_button = Label(root, text=f'{amount_played} users completed')
    amount_played_button.grid(column=3,row=0)

    #submit ratings
    diff_rating = tk.IntVar()
    diff_rating.set(10)
    diff_rating_menu = OptionMenu(root, diff_rating, 0,1,2,3,4,5,6,7,8,9,10)
    rating = tk.IntVar()
    rating.set(10)
    rating_menu = OptionMenu(root, rating, 0,1,2,3,4,5,6,7,8,9,10)
    rating_label = Label(root, text='Rating,Difficulty:')
    submit_rating_button = Button(root, text='Submit Ratings')
    submit_rating_button.bind("<Button-1>", submit_rating)

    #display ratings TODO: query for difficulty and user rating
    display_diff_rating = 8.2
    display_diff_rating_label = Label(root, text=f'Difficulty rating: {display_diff_rating}/10')
    display_diff_rating_label.grid(column=3,row=1, sticky='n')
    display_rating = 8.5
    display_rating_label = Label(root, text=f'User rating: {display_rating}/10')
    display_rating_label.grid(column=3,row=1)
    
    root.mainloop()
    #client.close()






if __name__ == "__main__":
    display_level('x','y')
