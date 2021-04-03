import pygame
import random, sys

WIDTH = 600
HEIGHT = 700
FPS = 30
TITLE = 'Tic Tac Toe'
TILE_WIDTH = 200
TILE_HEIGHT = 200

# define a few useful color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (220,220,220)
GREY = (150, 150, 150)


def check_win(board):
	freeSpace = []
	for j in range(len(board)):
		for i in range(len(board[1])):
			if board[j][i] == 0:
				freeSpace.append((j ,i))

	for i in range(3):
		if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != 0:
			return board[i][0], ('row', i)

		elif board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0:
			return board[0][i], ('col', i)

	if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
		return board[0][0], ('cross', 0)

	if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != 0:
		return board[0][2], ('cross', 2)

	if not freeSpace:
		return 3, 'none'

	return None, None

def minimax(board, depth, isMaximizer):
	scores = {1:-1, 2:1, 3:0}
	if depth == 0:
		return random.randrange(-1, 1)


	win = check_win(board)[0]
	if win:
		return scores[win]


	if isMaximizer:
		bestScore = -float('inf')
		for j in range(len(board)):
			for i in range(len(board[1])):
				if board[j][i] == 0:
					board[j][i] = 2
					score = minimax(board, depth - 1, False)
					board[j][i] = 0
					bestScore = max(bestScore, score)

		return bestScore

	else:
		bestScore = float('inf')
		for j in range(len(board)):
			for i in range(len(board[1])):
				if board[j][i] == 0:
					board[j][i] = 1
					score = minimax(board, depth - 1, True)
					board[j][i] = 0
					bestScore = min(bestScore, score)

		return bestScore


def text(message, screen, color, size, x, y, center = None):
	font = pygame.font.SysFont("Lucida Console", size)
	text = font.render(message, True, color)
	if center:
		screen.blit(text , (x- text.get_width() // 2, y - text.get_height() // 2))
	else:
		screen.blit(text, (x,y))

# win screen
class WinScreen:
		def __init__(self, super, message, pos):
			self.super = super
			self.screen = super.screen
			self.message = message
			self.pos = pos
			self.board = super.board
			self.againRect = pygame.Rect(180, 300, 240, 50)
			self.mainRect = pygame.Rect(190, 400, 220, 50)
			self.exitRect = pygame.Rect(240, 500, 120, 50)
			self.now = pygame.time.get_ticks()

		def run(self):
			self.running = True
			while self.running:
				self.super.clock.tick(FPS)
				self.events()
				self.update()


		def events(self):
			self.timer =  pygame.time.get_ticks()  - self.now
			for event in pygame.event.get():
				# check for closing the window
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN and self.timer >= 1500:
					if event.button == 1:
						if self.againRect.collidepoint(pygame.mouse.get_pos()):
							self.running = False
							self.super.new()

						elif self.exitRect.collidepoint(pygame.mouse.get_pos()):
							pygame.quit()
							sys.exit()

						elif self.mainRect.collidepoint(pygame.mouse.get_pos()):
							game = Main()
							game.new()

		def update(self):
			self.screen.fill(BACKGROUND)

			if self.timer < 1500:
				self.screen.blit(self.super.mainSurface, (0, 0))
				if self.pos[0] == 'row':
					pygame.draw.line(self.super.mainSurface, RED , (10 , self.pos[1] * TILE_HEIGHT + 100), (WIDTH - 10 , self.pos[1] * TILE_HEIGHT + 100) , 20)

				elif self.pos[0] == 'col':
					pygame.draw.line(self.super.mainSurface, RED , (self.pos[1] * TILE_WIDTH + 100, 10), (self.pos[1] * TILE_WIDTH + 100, HEIGHT - 110) , 20)

				elif self.pos[0] == 'cross':
					if self.pos[1] == 0:
						pygame.draw.line(self.super.mainSurface, RED , (0 , 0), (WIDTH, HEIGHT - 100) , 20)

					else:
						pygame.draw.line(self.super.mainSurface, RED , (0 , HEIGHT - 100), (WIDTH , 0) , 20)

				pygame.draw.rect(self.screen, GREY, (0 , 600, 600, 100))




			elif self.timer >= 1500:
				self.timer = 1000
				text(str(self.message), self.screen, BLACK, 50, 300, 200, True)

				pygame.draw.rect(self.screen, GREY, self.againRect, border_radius = 4)
				text('Play Again', self.screen, BLACK, 32, 300, 325, True)
				pygame.draw.rect(self.screen, GREY, self.mainRect, border_radius = 4)
				text('Main Menu', self.screen, BLACK, 32, 300, 425, True)
				pygame.draw.rect(self.screen, GREY, self.exitRect, border_radius = 4)
				text('Exit', self.screen, BLACK, 32, 300, 525, True)

			pygame.display.flip()

#2 Player
class PlayerVPlayer:
	def __init__(self, super):
		self.super = super
		self.screen = super.screen
		self.clock = self.super.clock

	def new(self):
		self.mainSurface = pygame.Surface((600, 600))
		self.mainSurface.fill(BACKGROUND)
		self.turn = 0
		self.board = [[0, 0, 0],
					[0, 0, 0],
					[0, 0, 0]]

		self.freeSpace = []
		for j in range(len(self.board)):
			for i in range(len(self.board[1])):
				if self.board[j][i] == 0:
					self.freeSpace.append((j , i))


		self.player = [1, 2]
		self.currentPlayer = self.player[self.turn]

		self.run()

	def run(self):
		self.running = True
		while self.running:
			self.clock.tick(FPS)
			self.events()
			self.update()


	def events(self):
		for event in pygame.event.get():
			# check for closing the window
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()



			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					x, y = pygame.mouse.get_pos()
					x = int(x // TILE_HEIGHT)
					y = int(y // TILE_WIDTH)

					if (y, x) in self.freeSpace:
						self.freeSpace.remove((y,x))
						self.board[y][x] = self.currentPlayer
						self.turn += 1
						self.currentPlayer = self.player[self.turn % len(self.player)]


	def update(self):
		self.screen.fill(BACKGROUND)

		self.screen.blit(self.mainSurface, (0, 0))

		pygame.draw.line(self.mainSurface, BLACK, (TILE_WIDTH, 0), (TILE_WIDTH, HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (TILE_WIDTH * 2, 0), (TILE_WIDTH * 2, HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (0, TILE_HEIGHT), (WIDTH, TILE_HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (0, TILE_HEIGHT * 2), (WIDTH, TILE_HEIGHT * 2), 4)

		for j in range(len(self.board)):
			for i in range(len(self.board[1])):
				if self.board[j][i] == 1:
					pygame.draw.circle(self.mainSurface, BLACK, (i * TILE_WIDTH + TILE_WIDTH // 2, j * TILE_HEIGHT + TILE_HEIGHT // 2), 80, 4)
				elif self.board[j][i] == 2:
					pygame.draw.line(self.mainSurface , BLACK, (i * TILE_WIDTH + 20, j * TILE_HEIGHT + 20), (i * TILE_WIDTH + 180, j * TILE_HEIGHT + 180) , 5)
					pygame.draw.line(self.mainSurface , BLACK, (i * TILE_WIDTH + 20, j * TILE_HEIGHT + 180), (i * TILE_WIDTH + 180, j * TILE_HEIGHT + 20) , 5)


		pygame.draw.rect(self.screen, GREY, (0 , 600, 600, 200))
		message = "X's Turn" if (self.turn % len(self.player)) else "O's Turn"
		text(message, self.screen, BLACK, 40, 300, 650 , True)


		win, pos = check_win(self.board)

		if win:
			self.running = False
			if win == 1:
				win_screen = WinScreen(self, "O is the winner", pos)
				win_screen.run()

			elif win == 2:
				win_screen = WinScreen(self, "X is the winner", pos)
				win_screen.run()

			else:
				win_screen = WinScreen(self, "Tie", pos)
				win_screen.run()

		pygame.display.flip()

# computer AI
class PlayerVComputer:
	def __init__(self, super, type):
		self.super = super
		self.screen = super.screen
		self.clock = self.super.clock
		self.type = type

	def new(self):
		self.mainSurface = pygame.Surface((600, 600))
		self.mainSurface.fill(BACKGROUND)
		self.board = [[0, 0, 0],
					[0, 0, 0],
					[0, 0, 0]]

		self.freeSpace = []
		for j in range(len(self.board)):
			for i in range(len(self.board[1])):
				if self.board[j][i] == 0:
					self.freeSpace.append((j , i))

		self.run()

	def run(self):
		self.running = True
		while self.running:
			self.clock.tick(FPS)
			self.events()
			self.update()


	def events(self):
		for event in pygame.event.get():
			# check for closing the window
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					x, y = pygame.mouse.get_pos()
					x = int(x // TILE_HEIGHT)
					y = int(y // TILE_WIDTH)

					if (y, x) in self.freeSpace:
						self.freeSpace.remove((y,x))
						self.board[y][x] = 1

						position = self.computer()

						if position:
							self.freeSpace.remove((position[0], position[1]))
							self.board[position[0]][position[1]] = 2

	def update(self):
		self.screen.fill(BACKGROUND)

		self.screen.blit(self.mainSurface, (0, 0))

		pygame.draw.line(self.mainSurface, BLACK, (TILE_WIDTH, 0), (TILE_WIDTH, HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (TILE_WIDTH * 2, 0), (TILE_WIDTH * 2, HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (0, TILE_HEIGHT), (WIDTH, TILE_HEIGHT), 4)
		pygame.draw.line(self.mainSurface, BLACK, (0, TILE_HEIGHT * 2), (WIDTH, TILE_HEIGHT * 2), 4)

		for j in range(len(self.board)):
			for i in range(len(self.board[1])):
				if self.board[j][i] == 1:
					pygame.draw.line(self.mainSurface , BLACK, (i * TILE_WIDTH + 20, j * TILE_HEIGHT + 20), (i * TILE_WIDTH + 180, j * TILE_HEIGHT + 180) , 5)
					pygame.draw.line(self.mainSurface , BLACK, (i * TILE_WIDTH + 20, j * TILE_HEIGHT + 180), (i * TILE_WIDTH + 180, j * TILE_HEIGHT + 20) , 5)
				elif self.board[j][i] == 2:
					pygame.draw.circle(self.mainSurface, BLACK, (i * TILE_WIDTH + TILE_WIDTH // 2, j * TILE_HEIGHT + TILE_HEIGHT // 2), 80, 4)


		pygame.draw.rect(self.screen, GREY, (0 , 600, 600, 200))
		text(self.type, self.screen, BLACK, 40, 300, 650 , True)


		win, pos = check_win(self.board)

		if win:
			self.running = False
			if win == 1:
				win_screen = WinScreen(self, "X is the winner", pos)
				win_screen.run()

			elif win == 2:
				win_screen = WinScreen(self, "O is the winner", pos)
				win_screen.run()

			else:
				win_screen = WinScreen(self, "Tie", pos)
				win_screen.run()

		pygame.display.flip()


	def computer(self):
		if check_win(self.board)[0]:
			return None

		# return random.choice(self.freeSpace)

		bestScore = -float('inf')
		bestMove = None
		for freeSpace in self.freeSpace:
			self.board[freeSpace[0]][freeSpace[1]] = 2
			if self.type == 'Easy':
				score = minimax(self.board, 7, False)
			else:
				score = minimax(self.board, 20, False)
			self.board[freeSpace[0]][freeSpace[1]] = 0

			if random.randrange(0, 100) < 50:
				if score >= bestScore:
					bestScore = score
					bestMove = freeSpace
			else:
				if score > bestScore:
					bestScore = score
					bestMove = freeSpace

		return bestMove

# Main menu
class Main:
	def __init__(self):
		pygame.init() #initialize pygame
		pygame.mixer.init() #initialize pygame sound
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		self.running = True


	def new(self):
		self.playerRect = pygame.Rect(140, 200, 320, 50)
		self.computerRect = pygame.Rect(120, 300, 360, 50)
		self.exitRect = pygame.Rect(240, 400, 120, 50)

		self.easyRect = pygame.Rect(240, 200, 120, 50)
		self.hardRect = pygame.Rect(240, 300, 120, 50)
		self.backRect = pygame.Rect(240, 400, 120, 50)

		self.selection = False

		self.run()

	def run(self):
		# game loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()

	def events(self):
		# game loop - events
		for event in pygame.event.get():
			# check for closing the window
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if not self.selection:
						if self.playerRect.collidepoint(pygame.mouse.get_pos()):
							self.playing = False
							game = PlayerVPlayer(self)
							game.new()

						elif self.computerRect.collidepoint(pygame.mouse.get_pos()):
							self.selection = True

						elif self.exitRect.collidepoint(pygame.mouse.get_pos()):
							pygame.quit()
							sys.exit()

					else:
						if self.easyRect.collidepoint(pygame.mouse.get_pos()):
							self.playing = False
							game = PlayerVComputer(self, 'Easy')
							game.new()

						elif self.hardRect.collidepoint(pygame.mouse.get_pos()):
							self.playing = False
							game = PlayerVComputer(self, 'Hard')
							game.new()

						elif self.backRect.collidepoint(pygame.mouse.get_pos()):
							self.selection = False

	def update(self):
		self.screen.fill(BACKGROUND)

		if not self.selection:

			pygame.draw.rect(self.screen, GREY, self.playerRect, border_radius = 4)
			text('Player vs Player', self.screen, BLACK, 32, 300, 225, True)
			pygame.draw.rect(self.screen, GREY, self.computerRect, border_radius = 4)
			text('Player vs Computer', self.screen, BLACK, 32, 300, 325, True)
			pygame.draw.rect(self.screen, GREY, self.exitRect, border_radius = 4)
			text('Exit', self.screen, BLACK, 32, 300, 425, True)

		else:
			pygame.draw.rect(self.screen, GREY, self.easyRect, border_radius = 4)
			text('Easy', self.screen, BLACK, 32, 300, 225, True)
			pygame.draw.rect(self.screen, GREY, self.hardRect, border_radius = 4)
			text('Hard', self.screen, BLACK, 32, 300, 325, True)
			pygame.draw.rect(self.screen, GREY, self.backRect, border_radius = 4)
			text('Back', self.screen, BLACK, 32, 300, 425, True)



		pygame.display.flip()


if __name__ == '__main__':
	game = Main()
	game.new()


pygame.quit()
