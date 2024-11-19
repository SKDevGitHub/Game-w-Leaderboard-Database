import tkinter as tk
from tkinter import messagebox
import server_request_handler as server
import display_level as dl
import user_page as du
import level_designer as ld

FONT = ("Verdana", 12)
def displayLanding(username):
    class landingPage(tk.Frame):
        def __init__(self, parent):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Landing Page", font=("Verdana", 16, "bold"))
            label.pack(pady=20)

            levelLabel = tk.Label(self, text = "Search Level", font = FONT)
            levelLabel.pack(pady=(10,0))
                            
            self.search_level = tk.Entry(self, font=FONT)
            self.search_level.pack(pady=(5,10))

            search_lbutton = tk.Button(self, text="Search Level", command=self.searchLevel)
            search_lbutton.pack(pady=(0,20))

            userLabel = tk.Label(self, text = "Search User", font = FONT)
            userLabel.pack(pady=(10,0))
            
            self.search_user = tk.Entry(self, font=FONT)
            self.search_user.pack(pady=(5,10))
            
            search_ubutton = tk.Button(self, text="Search User", command=self.searchUser)
            search_ubutton.pack(pady=(0,20))

            leveldesginbutton = tk.Button(self, text = "Level Designer", command = self.gotoLevelD)
            leveldesginbutton.pack(pady=(0,20))
        
        def searchLevel(self):
            levelName = self.search_level.get()
            search_level(levelName)
        
        def searchUser(self): 
            userName = self.search_user.get()
            search_user(userName)
        
        def gotoLevelD(self):
             ld.display_level_designer(username)

    def search_level(page_name):
            check = server.search_for_level(page_name)
            if len(check) != 0:
                print(f"CHECKER LEVEL: {check[0]}")
                dl.display_level(check[0], username)
            else:
                messagebox.showinfo("Level Not Found")
    
    def search_user(page_name):
            check = server.search_for_user(page_name)
            if len(check) != 0:
                print(f"CHECKER USERNAME: {check[0]}")
                du.displayUser(check[0])
            else:
                messagebox.showinfo("User Not Found")

    root = tk.Tk()
    root.title("Landing Page")
    root.geometry("400x400")

    landing = landingPage(root)
    landing.pack(fill = "both", expand = True)

    root.mainloop()
        

if __name__ == "__main__":
    username = "Stephen"
    server.connect("localhost", 2048)
    displayLanding(username)
