from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from stockfish import Stockfish
import chess

class ChessBot:
  def __init__(self):
    self.driver = None
    self.board = chess.Board()
    self.moves_list = []
    self.stockfish = Stockfish(path='../stockfish/stockfish-windows-x86-64-avx2.exe')


  def open_browser(self, event=None):
    self.driver = webdriver.Chrome()

    self.driver.get('https://www.chess.com/play/computer/CoachDannyBot')

    input()

    self.driver.quit()


  def get_moves(self):
    self.moves_list = [] # reset list

    move_container = self.driver.find_element(By.XPATH, '//*[@id="scroll-container"]/wc-vertical-move-list')
    moves = move_container.find_elements(By.CSS_SELECTOR, 'div.move [data-ply]')
    
    for move in moves:
      move_class = move.get_attribute("class")

      if "white node" in move_class or "black node" in move_class:
        self.moves_list.append(move.text)

  
  def get_best_move(self):
    self.get_moves()
    self.board.reset()

    for move in self.moves_list:
      self.board.push_san(move)

    move_list_uci = [move.uci() for move in self.board.move_stack]

    self.stockfish.set_position(move_list_uci)

    return self.stockfish.get_best_move()

  
  def run_bot(self, event=None):
    best_move = self.get_best_move()

    print(best_move)




