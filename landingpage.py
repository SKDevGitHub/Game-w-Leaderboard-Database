import tkinter as tk

#from game_page import launchGame
#from user_page import UserPage

FONT = ("Verdana", 12)

class landingPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        label = tk.Label(self, text = "Landing Page", font = FONT)
        label.pack(pady = 10, padx = 10)
        
        self.search_level = tk.Entry(self, font = FONT)
        self.level_entry.pack(pady = 10)
        
        self.search_user = tk.Entry(self, font = FONT)
        self.user_entry.pack(pady = 10)
        
        search_lbutton = tk.Button(self, text="Search Level", command=lambda: self.searchLevel(controller))
        search_lbutton.pack()
        
        search_ubutton = tk.Button(self, text="Search User", command=lambda: self.searchUser(controller))
        search_ubutton.pack()
    
    def search_page(self, page_name):
        # Check if the page exists in the `page_names` dictionary
        page_class = self.page_names.get(page_name.lower())
        if page_class:
            self.show_frame(page_class)
        else:
            print("Page not found")
    
    def searchLevel(self, controller):
        levelName = self.search_level.get()
        controller.search_page(levelName)
    
    def searchUser(self, controller): 
        userName = self.search_user.get()
        controller.search_page(userName)
        
    def main():
        # Initialize Tkinter root window
        root = tk.Tk()
        root.title("Landing Page")

        def search_page(page_name):
        # Check if the page exists in the page_names dictionary
        page_class = self.page_names.get(page_name.lower())
        if page_class:
            self.show_frame(page_class)
        else:
            print("Page not found")
    
        # Initialize and display the landing page
        landing = landingPage(root, search_page)
        landing.pack()
    
        # Run the Tkinter main loop
        root.mainloop()

if __name__ == "__main__":
    main()
