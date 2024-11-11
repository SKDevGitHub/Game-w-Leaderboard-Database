import tkinter as tk

FONT = ("Verdana", 12)

class landingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Landing Page", font=FONT)
        label.pack(pady=10, padx=10)
        
        # Level Search Entry
        self.search_level = tk.Entry(self, font=FONT)
        self.search_level.pack(pady=10)
        
        # User Search Entry
        self.search_user = tk.Entry(self, font=FONT)
        self.search_user.pack(pady=10)
        
        # Buttons for Search
        search_lbutton = tk.Button(self, text="Search Level", command=self.searchLevel)
        search_lbutton.pack()
        
        search_ubutton = tk.Button(self, text="Search User", command=self.searchUser)
        search_ubutton.pack()
    
    def searchLevel(self):
        levelName = self.search_level.get()
        self.controller(levelName)
    
    def searchUser(self): 
        userName = self.search_user.get()
        self.controller(userName)

def main():
    # Define page names mapping
    page_names = {
        "game": "GamePage",  # Replace with actual class if available
        "user": "UserPage"   # Replace with actual class if available
    }

    # Define the function to handle page search
    def search_page(page_name):
        page_class = page_names.get(page_name.lower())
        if page_class:
            print(f"Navigating to: {page_class}")  # Placeholder for navigation
        else:
            print("Page not found")

    # Initialize Tkinter root window
    root = tk.Tk()
    root.title("Landing Page")

    # Initialize and display the landing page
    landing = landingPage(root, search_page)
    landing.pack()

    # Run the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
