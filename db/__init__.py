"""
This is sample of database storage file
need using postgree for example
"""

USERS = {
  0: {'login': 'user0', 'password': 'pass0'},
  1: {'login': 'user1', 'password': 'pass1'},
  2: {'login': 'user2', 'password': 'pass2'},
  3: {'login': 'user3', 'password': 'pass3'},
  4: {'login': 'user4', 'password': 'pass4'},
}


GAMES = {
  0: {'players': [0, 1, 3], 'tokens': []},
  1: {'players': [2, 4], 'tokens': []},
}
