import tkinter
import customtkinter
from main import open_browser, start_autoplay

# system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

# app frame
app = customtkinter.CTk()
app.geometry("480x480")
app.title('Chess AI')

# font settings
button_font = ("Roboto", 16, "bold")

# ui elements
open_browser_btn = customtkinter.CTkButton(app, text="Open Browser", width=200, height=50, command=open_browser, font=button_font)
open_browser_btn.pack(anchor='w', padx=10, pady=(10, 0))

start_autoplay_btn = customtkinter.CTkButton(app, text="Start Autoplay", width=200, height=50, command=start_autoplay, font=button_font)
start_autoplay_btn.pack(anchor='w', padx=10, pady=(10, 0))

# run app
app.mainloop()


