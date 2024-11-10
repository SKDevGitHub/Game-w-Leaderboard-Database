#import individual files here

display_page = "login"

while True:
    if display_page == "login":
        
        username = display_login()
        #this will only finish after the user logs in or registers
        display_page = "landing"
    
    elif display_page == "landing":
        next_page, parameter = display_landing()

        if next_page == "user":
            display_user(parameter)
        
        elif next_page == "level":
            display_level(parameter, username)
        
        elif next_page == "login":
            display_page = "login"
            username = None

        elif next_page == "level_designer":
            display_page = "level_designer"
    
    elif display_page == "level_designer":
        display_level_designer()
        #go back to landing afterwards
        display_page = "landing"
    
    elif display_page == "quit" or username == None:
        break