import customtkinter

from chessbot import ChessBot

class GUI:
  def __init__(self, app):
    self.app = app
    self.chess_bot = ChessBot()

    app.geometry("480x480")
    app.title("Chess AI Bot")
    
    self.button_font = ("Roboto", 16, "bold")

    self.open_browser_btn = customtkinter.CTkButton(app, text="Open Browser", width=200, height=50, command=self.chess_bot.open_browser, font=self.button_font)
    self.open_browser_btn.pack(anchor='w', padx=10, pady=(10, 0))

    self.run_bot_btn = customtkinter.CTkButton(app, text="Run Bot", width=200, height=50, command=self.chess_bot.run_bot, font=self.button_font)
    self.run_bot_btn.pack(anchor='w', padx=10, pady=(10, 0))


if __name__ == "__main__":
  customtkinter.set_appearance_mode("System")
  customtkinter.set_default_color_theme("green")
  
  app = customtkinter.CTk()
  gui = GUI(app)
  app.mainloop()