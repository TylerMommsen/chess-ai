from selenium import webdriver
from selenium.webdriver.common.by import By
from stockfish import Stockfish
import chess
import pyautogui

class ChessBot:
  def __init__(self):
    self.driver = None
    self.board = chess.Board()
    self.stockfish = Stockfish(path='../stockfish/stockfish-windows-x86-64-avx2.exe')


  # open up a chrome browser
  def open_browser(self, event=None):
    options = webdriver.ChromeOptions()
    self.driver = webdriver.Chrome(options=options)
    self.driver.get('https://www.chess.com/play/computer/CoachDannyBot')
    input()
    self.driver.quit()


  # get the board element
  def get_board(self):
    return self.driver.find_element(By.XPATH, "//*[@id='board-play-computer']")


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
    x_index = column_to_index[column]
    y_index = 8 - row

    # get the exact coordinates for the center of the square
    x_pos = board_pos_x + (square_size * x_index) + (square_size / 2)
    y_pos = board_pos_y + (square_size * y_index) + (square_size / 2)

    return (x_pos, y_pos)
  

  # click and drag piece to the next best position
  def make_move(self, source, target):
    print(source, target)
    start_pos = self.get_square_center(source)
    end_pos = self.get_square_center(target)

    pyautogui.moveTo(start_pos[0], start_pos[1])
    pyautogui.dragTo(end_pos[0], end_pos[1])


  # get the real game updated/new moves and apply them to the internal board
  def update_moves(self):
    move_container = self.driver.find_element(By.XPATH, '//*[@id="scroll-container"]/wc-vertical-move-list')
    moves = move_container.find_elements(By.CSS_SELECTOR, 'div.move [data-ply]')
    
    new_moves = [move.text for move in moves if "white node" in move.get_attribute("class") or "black node" in move.get_attribute("class")]
    last_known = len(self.board.move_stack)

    # apply only new moves to the internal board
    for move in new_moves[last_known:]:
      self.board.push_san(move)

  
  # get the next best move
  def get_next_best_move(self):
    self.update_moves()

    # set the position for stockfish with our new/updated internal board
    moves_list_uci = [move.uci() for move in self.board.move_stack]
    self.stockfish.set_position(moves_list_uci)

    # get the best move from stockfish given our current position
    best_move = self.stockfish.get_best_move()
    if best_move:
      source = best_move[:2]
      target = best_move[2:4]
      return source, target
    return None, None

  
  def run_bot(self, event=None):
    source, target = self.get_next_best_move()

    self.make_move(source, target)

    print(f"Moved from {source} to {target}")




