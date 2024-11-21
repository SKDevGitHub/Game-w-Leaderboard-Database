#import individual files here
from landingpage import displayLanding
import login
import display_level as dl
import level_designer as ld
import user_page as up
import server_request_handler as query

display_page = "login"
query.connect('localhost',2048)
while True:
    if display_page == "login":
        
        username = login.display_login()
        #this will only finish after the user logs in or registers
        if username != None:
            display_page = "landing"
        else:
            break
    
    elif display_page == "landing":
        next_page, parameter = displayLanding(username)

        if next_page == "user":
            up.displayUser(parameter)
        
        elif next_page == "level":
            dl.display_level(parameter, username)
        
        elif next_page == "login":
            display_page = "login"
            username = None

        elif next_page == "designer":
            display_page = "designer"
        else:
            break
    
    elif display_page == "designer":
        ld.display_ld(username)
        #go back to landing afterwards
        display_page = "landing"
    
    elif display_page == None or username == None:
        break


query.close_connection()