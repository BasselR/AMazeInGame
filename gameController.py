import pygame
#Standard lib
# import os
# import sys
# import time
# import random
# import math
#Own Files
import map
import minigame
import minigameContainer
import player
import mapController
import minigameController
import playerController
import gameDisplay
#import dataTypes

# pygame.init()
# height = 320
# width = 320
# window = pygame.display.set_mode((height,width),pygame.RESIZABLE)
# pygame.display.set_caption('AMazeInGame!')
# screen = pygame.display.get_surface()
# screen.convert_alpha()
# clock = pygame.time.Clock()

class GameController():
	def __init__(self):
		self.md = map.MapData()
		self.pd = player.PlayerData()
		self.mgd = minigameContainer.MinigameData()

		self.mc = mapController.MapController()
		self.pc = playerController.PlayerController()
		self.mgc = minigameController.MinigameController()

		self.inMap = True
		self.minigameNum = -1
		self.pause = False

		self.disp = gameDisplay.GameDisplay()

	def startGame(self):
		self.mc.set(self)
		self.pc.set(self)
		self.mc.startMap()
		self.pc.startPlayer()

	def exitGame(self):
		self.mc.exitMap()
		self.pc.exitPlayer()
		self.mgc.exitMinigame()

	def pauseGame(self):
		self.pause = not(self.pause)
		self.mc.pauseMap()
		self.pc.pausePlayer()
		self.mgc.pauseMinigame()

	def sendPlayerData(self, playerData):
		self.pd = playerData

		if self.inMap:
			self.md = self.mc.fetchMapData()
			self.pmInteraction()
		else:
			self.mgd = self.mgc.fetchMinigameData(self.minigameNum)
			self.pmgInteraction()

	def sendMapData(self, mapData):
		self.md = mapData
		self.pd = self.pc.fetchPlayerData()

		self.pmInteraction()

	def sendMinigameData(self, minigameData):
		self.mgd = minigameData
		self.pd = self.pc.fetchPlayerData()

		self.pmgInteraction()

	def pmInteraction(self):
		self.playerMInteraction()
		self.mapInteraction()

		self.mc.updateMapData(self.md)
		self.pc.updatePlayerData(self.pd)

		if self.inMap:
			self.disp.displayMap(self.pd, self.md)
		else:
			self.mgc.startMinigame(self.minigameNum)

	def pmgInteraction(self):
		self.playerMgInteraction()
		if self.minigameNum == 2:
			self.minigame2Interaction()

		self.mgc.updateMinigameData(self.minigameNum, self.mgd)
		self.pc.updatePlayerData(self.pd)

		self.disp.displayMinigame(self.pd, self.mgd)


		if self.inMap:
			self.mgc.exitMinigame()
			self.minigameNum = -1
			self.pd.x = 0
			self.pd.y = 0
			self.pd.score = 0

	def mapInteraction(self):
		for i in self.md.stars:
			if self.pd.x == i[0][0] and self.pd.y == i[0][1] and self.inMap:
				print("enter minigame ", i[1])
				self.inMap = False
				self.minigameNum = i[1]
				self.pd.x = 0
				self.pd.y = 0
		pass

	def minigameInteraction(self):

		# exit minigame
		if self.pd.x == 4 and self.pd.y == 4 and not(self.inMap):
			print("exit minigame")
			self.inMap = True
			self.minigameNum = -1

	def playerMInteraction(self):

		#player movement in map
		x = self.pd.x + self.pd.xs
		y = self.pd.y + self.pd.ys
		if x >= 0 and x < self.md.width and y >= 0 and y < self.md.height and self.md.tiles[x][y] != 'w':
			self.pd.x += self.pd.xs
			self.pd.y += self.pd.ys

		self.pd.xs = 0
		self.pd.ys = 0

	def playerMgInteraction(self):

		#exit minigame
		if self.mgd.end != 0 and self.pd.x == self.mgd.exit[0] and self.pd.y == self.mgd.exit[1]:
			print("exit minigame")
			self.inMap = True

		#player movement in minigame

		x = self.pd.x + self.pd.xs
		y = self.pd.y + self.pd.ys
		if x >= 0 and x < self.mgd.width and y >= 0 and y < self.mgd.height and self.mgd.tiles[y][x] != 'w':
			self.pd.x += self.pd.xs
			self.pd.y += self.pd.ys
			if self.pd.xs != 0 and self.pd.ys != 0:
				print("move")

		self.pd.xs = 0
		self.pd.ys = 0

		#item pickup

		temp = []
		for i in self.mgd.items:
			if (i.x == self.pd.x and i.y == self.pd.y):
				self.pd.score += i.value
			else:
				temp.append(i)

		self.mgd.items = temp


	def minigame2Interaction(self):

		# end minigame
		if self.mgd.items == []:
			if self.pd.score >= self.mgd.bots[0].score:
				self.mgd.end = 1
			else:
				self.mgd.end = -1

		# run bots

		for i in self.mgd.bots:
			if i.timer == 0:
				x = i.path[0][0]
				y = i.path[0][1]
				p = ((x / abs(x)) if x != 0 else 0, (y / abs(y)) if y != 0 else 0)
				p = (p[0] * i.speed, p[1] * i.speed)
				i.path[0][0] -= p[0]
				i.path[0][1] -= p[1]
				if i.path[0] == [0, 0]:
					del i.path[0]
					if i.path == []:
						for j in i.track:
							i.path.append(j.copy())
				i.x += p[0]
				i.y += p[1]
				i.timer = i.cd

				temp = []
				for j in self.mgd.items:
					if (j.x == i.x and j.y == i.y):
						i.score += j.value
					else:
						temp.append(j)

				self.mgd.items = temp
			else:
				i.timer -= 1

			


