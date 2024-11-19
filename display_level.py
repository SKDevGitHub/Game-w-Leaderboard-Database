from tkinter import Button, Label, Tk, Scrollbar, Entry, Listbox, OptionMenu
import tkinter as tk
import server_request_handler as query
import dungeonCrawler



def display_level(levelname, username):
    
    def play_game(event):
        #TODO 
        gamedata = dungeonCrawler.displayLevel(leveldata[0])
        display_rating_section()
        if gamedata[0] != 0: #they beat the level
            query.submit_solution(username,levelname,gamedata[1],gamedata[0])
            leaderboard_data = query.leaderboard_data_query(levelname)
    def display_rating_section():
        diff_rating_menu.grid(column=6,row=1,sticky='e')
        rating_menu.grid(column=6,row=1,sticky='w')
        rating_label.grid(column=6,row=1,sticky='n')
        submit_rating_button.grid(column=6, row=2,sticky='n')


    def submit_rating(event):
        query.rate_level(username, rating.get(),diff_rating.get(), levelname)

        rating_menu.destroy()
        rating_label.destroy()
        diff_rating_menu.destroy()
        submit_rating_button.destroy()
        play_level_button.destroy()
        

    def display_leaderboard(event):
        lb = Tk()
        lb.title(f'{levelname} leaderboard')
        lb.geometry("400x200")

        lb.columnconfigure((0,1),weight=1)
        lb.rowconfigure((0,1),weight=1)

        leaderboard = Listbox(lb, selectmode='single')
        leaderboard.grid(row=0,column=0,sticky='nswe',rowspan=2,columnspan=2)
        lb_scroller = Scrollbar(lb, orient='vertical',command=leaderboard.yview)
        lb_scroller.grid(row=0,rowspan=2,column=1,sticky='nes')

        #insert leaderboard tuples
        rank = 1
        for tuple in leaderboard_data:
            leaderboard.insert('end',f'{rank}. Username: {tuple[0]}, Score: {tuple[1]}, Date: {tuple[2][:10]}')
            rank = rank + 1
        if leaderboard_data == []:
            leaderboard.insert('end', 'No users have completed this level')
        

        #TODO: do i need this?
        root.quit()
        return "quit"

    def go_back(event):
        root.destroy()

    def add_comment(event):
        text = comment_entry.get()
        comment_entry.delete(0, tk.END)

        query.create_comment(text,username,levelname)

    def like_comment(event):
        index = comment_box.curselection()
        index = index[0]
        comment_id = comments[index][3]
        query.like_comment(comment_id)

    def dislike_comment(event):
        index = comment_box.curselection()
        index = index[0]

        comment_id = comments[index][3]
        query.dislike_comment(comment_id)
    
    #query for comments
    comments = query.get_level_comments(levelname)


    #create gui
    root = Tk()
    root.title("Dungeon Crawler")
    root.geometry('800x600')
    root.rowconfigure((0,1,2), weight=1)
    root.rowconfigure(3, weight=3)
    root.columnconfigure((0,1,2,3,4,5,6),weight=1)
    leveldata = query.get_level_data(levelname)
    creator = leveldata[1]

    #comments section init
    comment_box = Listbox(root, selectmode=tk.SINGLE)
    comment_box.grid(row=3, sticky='nsew',columnspan=7)
    for c in comments:
        comment_box.insert('end', f'{c[4]} says: {c[2]} -> {c[0]} likes, {c[1]} dislikes')
    if comments == []:
        comment_box.insert('end', "No Comments Yet")
    
    #scrollbars
    scroller = Scrollbar(root, orient='vertical', command=comment_box.yview)
    scroller.grid(row=3,column=6, sticky="nse")
    comment_box.config(yscrollcommand=scroller.set)
    yscroller = Scrollbar(root, orient='horizontal',command=comment_box.xview)
    yscroller.grid(column=0,columnspan=7,row=3,sticky='wse')

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
    leaderboard_data = query.leaderboard_data_query(levelname)
    leaderboard_data.sort(key = lambda x: x[1], reverse= True)
    leaderboard_button = Button(root,text="View Leaderboard")
    leaderboard_button.bind("<Button-1>", display_leaderboard)
    leaderboard_button.grid(row=1,column=0,sticky='s')

    #amount of users played
    amount_played = len(leaderboard_data)
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

    #display ratings
    ratings = query.get_level_ratings(levelname)
    display_diff_rating = ratings[1]
    display_diff_rating_label = Label(root, text=f'Difficulty rating: {display_diff_rating:.2f}/10')
    display_diff_rating_label.grid(column=3,row=1, sticky='n')
    display_rating = ratings[0]
    display_rating_label = Label(root, text=f'User rating: {display_rating:.2f}/10')
    display_rating_label.grid(column=3,row=1)

    #display level creator
    creator_label = Label(root,text=f'Creator: {creator}')
    creator_label.grid(row=0,column=3,sticky='s')
    
    root.mainloop()







if __name__ == "__main__":
    query.connect('localhost', 2048)
    display_level('joe miners bad day','Ben')
    query.close_connection()
