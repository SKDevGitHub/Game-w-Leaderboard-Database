import tkinter as tk
import server_request_handler as server
import display_level as dl
import user_page as du

FONT = ("Verdana", 12)

def displayLanding(username):
    class landingPage(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="Landing Page", font=("Verdana", 16, "bold"))
            label.pack(pady=20)

            levelLabel = tk.Label(self, text = "Search Level", font = FONT)
            levelLabel.pack(pady=(10,0))
                            
            self.search_level = tk.Entry(self, font=FONT)
            self.search_level.pack(pady=(5,10))

            search_lbutton = tk.Button(self, text="Search User", command=self.searchLevel)
            search_lbutton.pack(pady=(0,20))

            userLabel = tk.Label(self, text = "Search Level", font = FONT)
            userLabel.pack(pady=(10,0))
            
            self.search_user = tk.Entry(self, font=FONT)
            self.search_user.pack(pady=(5,10))
            
            search_ubutton = tk.Button(self, text="Search User", command=self.searchUser)
            search_ubutton.pack(pady=(0,20))
        
        def searchLevel(self):
            levelName = self.search_level.get()
            self.controller(levelName)
        
        def searchUser(self): 
            userName = self.search_user.get()
            self.controller(userName)

    page_names = {
        "game": "GamePage", 
        "user": "UserPage"  
    }

    def search_page(page_name):
        page_class = page_names.get(page_name.lower())
        if page_class:
            print(f"Navigating to: {page_class}")  
        else:
            print("Page not found")

    root = tk.Tk()
    root.title("Landing Page")
    root.geometry("400x400")

    landing = landingPage(root, search_page)
    landing.pack(fill = "both", expand = True)

    root.mainloop()

if __name__ == "__main__":
    username = "root"
    server.connect("localhost", 2048)
    displayLanding(username)
