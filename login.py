import tkinter as tk
from tkinter import messagebox
from server_request_handler import login,register,connect
# Uploaded Customized login page. Still have the non-customized if you want to revert back
def display_login():
    user_logged_in = None

    # Function for the login button
    def process_login():
        nonlocal user_logged_in
        username = username_entry.get()
        password = password_entry.get()

        if login(username, password):  # True if login is successful
            user_logged_in = username
            messagebox.showinfo("Login Success", "You have successfully logged in!")
            login_register_window.destroy()  # Closes the login window
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    # Function for the register button
    def process_register():
        nonlocal user_logged_in
        username = username_entry.get()
        password = password_entry.get()

        if register(username, password):  # True if registration is successful
            user_logged_in = username
            messagebox.showinfo("Registration Success", "You have successfully registered!")
            login_register_window.destroy()  # Closes the registration window
        else:
            messagebox.showerror("Registration Failed", "Username already exists or another error occurred.")

    # Set up the main login/register window
    login_register_window = tk.Tk()
    login_register_window.title("ACT MAN ONLINE")
    login_register_window.geometry("400x300")
    login_register_window.configure(bg="black")  # Set background to black

    # Add a title label
    title_label = tk.Label(
        login_register_window, 
        text="ACT MAN ONLINE", 
        font=("TkDefaultFont", 24, "bold"), 
        bg="black", 
        fg="red"
    )
    title_label.pack(pady=(20, 10))

    # Create a frame for the input fields with dark red background
    frame = tk.Frame(login_register_window, bg="#8B0000", bd=2, relief="solid")
    frame.pack(pady=10, padx=20)

    # Username input
    username_label = tk.Label(
        frame, 
        text="USERNAME:", 
        font=("TkDefaultFont", 12, "bold"), 
        bg="#8B0000", 
        fg="black"
    )
    username_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    username_entry = tk.Entry(frame, font=("TkDefaultFont", 12), width=20, bd=0, bg="black", fg="red", insertbackground="red")
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    # Password input
    password_label = tk.Label(
        frame, 
        text="PASSWORD:", 
        font=("TkDefaultFont", 12, "bold"), 
        bg="#8B0000", 
        fg="black"
    )
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    password_entry = tk.Entry(frame, font=("TkDefaultFont", 12), show="*", width=20, bd=0, bg="black", fg="red", insertbackground="red")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    # Buttons
    button_frame = tk.Frame(login_register_window, bg="black")
    button_frame.pack(pady=10)

    # Register button
    register_button = tk.Button(
        button_frame, 
        text="REGISTER", 
        command=process_register, 
        font=("TkDefaultFont", 12, "bold"), 
        bg="#8B0000", 
        fg="black", 
        width=10, 
        bd=0, 
        highlightthickness=0,
        activebackground="red",
        activeforeground="black"
    )
    register_button.grid(row=0, column=0, padx=5)

    # Login button
    login_button = tk.Button(
        button_frame, 
        text="LOGIN", 
        command=process_login, 
        font=("TkDefaultFont", 12, "bold"), 
        bg="#8B0000", 
        fg="black", 
        width=10, 
        bd=0, 
        highlightthickness=0,
        activebackground="red",
        activeforeground="black"
    )
    login_button.grid(row=0, column=1, padx=5)

    # Start the Tkinter event loop
    login_register_window.mainloop()

    return user_logged_in