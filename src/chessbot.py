from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from stockfish import Stockfish
import chess
import pyautogui
import time

class ChessBot:
  def __init__(self):
    self.driver = None
    self.board = chess.Board()
    self.stockfish = Stockfish(path='../stockfish/stockfish-windows-x86-64-avx2.exe')
    self.playing_as_white = None
    self.move_list_container = None
    self.last_processed_move = 0 # tracks the last ply number processed


  # open up a chrome browser
  def open_browser(self, event=None):
    options = webdriver.ChromeOptions()
    self.driver = webdriver.Chrome(options=options)
    self.driver.get('https://www.chess.com')
    input()
    self.driver.quit()


  # get the board element
  def get_board(self):
    board = None
    try:
      board = self.driver.find_element(By.XPATH, "//*[@id='board-play-computer']")
    except NoSuchElementException:
      try:
        board = self.driver.find_element(By.XPATH, '//*[@id="board-single"]')
      except NoSuchElementException:
        board = None
      
  
    return board
  
  
  def is_white(self):
    all_squares = None

    try:
      coordinates = self.driver.find_element(By.XPATH, "//*[@id='board-play-computer']//*[name()='svg']")
      all_squares = coordinates.find_elements(By.XPATH, ".//*")
    except NoSuchElementException:
      try:
        coordinates = self.driver.find_elements(By.XPATH, "//*[@id='board-single']//*[name()='svg']")
        coordinates = [x for x in coordinates if x.get_attribute("class") == "coordinates"][0]
        all_squares = coordinates.find_elements(By.XPATH, ".//*")
      except NoSuchElementException:
        return None
      
    elem = None
    x_pos = None
    y_pos = None

    for i in range(len(all_squares)):
      name_element = all_squares[i]
      x = float(name_element.get_attribute("x"))
      y = float(name_element.get_attribute("y"))

      if i == 0 or (x <= x_pos and y >= y_pos):
        x_pos = x
        y_pos = y
        elem = name_element

    if elem.text == "1":
      self.playing_as_white = True
    else:
      self.playing_as_white = False


  def get_square_center(self, square):
    # get location of the top left of the website
    site_pos_x = self.driver.execute_script("return window.screenX + (window.outerWidth - window.innerWidth) / 2 - window.scrollX;")
    site_pos_y = self.driver.execute_script("return window.screenY + (window.outerHeight - window.innerHeight) - window.scrollY;")

    # get location of the board
    board_pos = self.get_board().location
    board_pos_x = site_pos_x + board_pos["x"]
    board_pos_y = site_pos_y + board_pos["y"]

    # get the size of the squares
    square_size = self.get_board().size['width'] / 8

    column_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    # extract the column and row from the square position (for example e2, column = e, row = 2)
    column = square[0]
    row = int(square[1])

    # get the x,y int value for the corresponding square
    if self.playing_as_white:
      x_index = column_to_index[column]
      y_index = 8 - row
    else:
      x_index = 8 - column_to_index[column] - 1
      y_index = row - 1

    # get the exact coordinates for the center of the square
    x_pos = board_pos_x + (square_size * x_index) + (square_size / 2)
    y_pos = board_pos_y + (square_size * y_index) + (square_size / 2)

    return (x_pos, y_pos)
  

  # click and drag piece to the next best position
  def make_move(self, best_move):
    start_pos = self.get_square_center(best_move[:2])
    end_pos = self.get_square_center(best_move[2:4])

    pyautogui.moveTo(start_pos[0], start_pos[1])
    pyautogui.dragTo(end_pos[0], end_pos[1])

    # check for a piece promotion
    if len(best_move) == 5:
      time.sleep(0.1)
      x_pos = None
      y_pos = None
      if best_move[4] == 'q':
        x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3])))
      elif best_move[4] == 'n':
        if self.playing_as_white:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) - 1))
        else:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) + 1))
      elif best_move[4] == 'r':
        if self.playing_as_white:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) - 2))
        else:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) + 2))
      elif best_move[4] == 'b':
        if self.playing_as_white:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) - 3))
        else:
          x_pos, y_pos = self.get_square_center(best_move[2] + str(int(best_move[3]) + 3))

      pyautogui.moveTo(x_pos, y_pos)
      pyautogui.click(button='left')

  # get the container which contains all the moves made
  def set_move_list_container(self):
    move_container = None
    try:
      move_container = self.driver.find_element(By.CLASS_NAME, "play-controller-scrollable")
    except NoSuchElementException:
      try:
        move_container = self.driver.find_element(By.CLASS_NAME, "move-list-wrapper-component")
      except NoSuchElementException:
        self.move_list_container = None
      
    self.move_list_container = move_container


  # get the real game updated/new moves and apply them to the internal board
  def update_moves(self):
    css_selector = f'div.move [data-ply="{self.last_processed_move + 1}"]'
    new_moves = self.move_list_container.find_elements(By.CSS_SELECTOR, css_selector)

    # apply only new moves to the internal board
    for move in new_moves:
      if "white node" in move.get_attribute('class') or "black node" in move.get_attribute("class"):
        move_text = move.text
        move_ply = int(move.get_attribute('data-ply'))
      
        try:
          child = move.find_element(By.XPATH, "./*")
          move_figurine = child.get_attribute("data-figurine")
        except NoSuchElementException:
          move_figurine = None
        
        if move_figurine:
          full_move = move_figurine + move_text
        else:
          full_move = move_text

        self.board.push_uci(self.board.parse_san(full_move).uci())

        self.last_processed_move = move_ply

        print(move_ply)
        print(full_move)

  
  # get the next best move
  def get_next_best_move(self):
    # set the position for stockfish with our new/updated internal board
    moves_list_uci = [move.uci() for move in self.board.move_stack]
    self.stockfish.set_position(moves_list_uci)

    # get the best move from stockfish given our current position
    best_move = self.stockfish.get_best_move()
    if best_move:
      return best_move
    
    return None


  # start the bot loop until checkmate is reached
  def run_bot(self, event=None):
    self.board.reset() # set up board to default position
    self.is_white() # determine if you are playing as white or black
    self.set_move_list_container()

    while True:
      self.update_moves()

      if (self.board.turn == chess.WHITE and self.playing_as_white) or (self.board.turn == chess.BLACK and not self.playing_as_white):
        # make move for yourself
        best_move = self.get_next_best_move()
        self.make_move(best_move)
        self.update_moves()


      if self.board.is_checkmate():
        self.last_processed_move = 0
        break


      # wait for opponent to make move
      css_selector = f'div.move [data-ply="{self.last_processed_move + 1}"]'
      while True:
        time.sleep(0.1)
        new_moves = self.move_list_container.find_elements(By.CSS_SELECTOR, css_selector)

        if new_moves:
          self.update_moves()
          break

      if self.board.is_checkmate():
        self.last_processed_move = 0
        break
