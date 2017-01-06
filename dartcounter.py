#!/usr/bin/env python

import sys
import curses

screen = None
width = 0
height = 0

def initCurses():
	global screen
	global width
	global height
	
	screen = curses.initscr()
	height, width = screen.getmaxyx()
	curses.noecho()
	screen.keypad(True)
	
	
def endCurses():
	curses.echo()
	curses.endwin()
	
def askForInitPoints():
	curses.echo()
	screen.addstr(height-2,0,"How many points?")
	ret = screen.getstr(height-1,0,4)
	i = int(ret)
	curses.noecho()
	screen.refresh()
	return i
	
def displayBoard(playerOrder, playerScores, initPoints):
	curoffset = 0
	for player in playerOrder:
		offsetAdd = max(len(player)+5,16)
		if len(playerScores[player]) > 0:
			avg = sum(playerScores[player]) / len(playerScores[player])
		else:
			avg = 0
		screen.addstr(0,curoffset,player)
		screen.addstr(1,curoffset,"Avg: %.2f" % avg)
		screen.addstr(2,curoffset,'#' * offsetAdd)
		screen.addstr(3,curoffset,str(initPoints))
		cl = 4
		curpoints = initPoints
		for p in playerScores[player]:
			curpoints = curpoints - p
			screen.addstr(cl,curoffset,str(curpoints))
			cl = cl+1
			
		curoffset = curoffset + offsetAdd
	screen.refresh()

def clearLine(lineIndex):
	screen.addstr(lineIndex,0,' '*(width-1))

def askForNumber(question):
	curses.echo()
	clearLine(height-1)
	clearLine(height-2)
	screen.addstr(height-2,0,question)
	screen.refresh()
	ret = ""
	while not ret:
		ret = screen.getstr(height-1,0,3)
	i = int(ret)
	curses.noecho()
	return i

def main():
	players = list()
	for n in sys.argv[1:]:
		players.append(n)
		
	
	checkouts = dict()
	with open("checkout.csv","r") as f:
		lines=f.readlines()
		for line in lines:
			spl = line.split(",")
			checkouts[int(spl[0])] = list()
			for e in spl[1:]:
				checkouts[int(spl[0])].append(e)
	
	initCurses()
	initPoints = askForNumber("How many points?")

	playerScores = {p: list() for p in players}
	
	displayBoard(players,playerScores,initPoints)
	
	finished = False
	winner = ""
	while not finished:
		for player in players:
			points = initPoints - sum(playerScores[player])
			clearLine(height-3) 
			if points in checkouts.keys():
				note = "Possible checkout for "+player+":"
				screen.addstr(height-3,0,note)
				index = len(note)+1
				for e in checkouts[points]:
					screen.addstr(height-3,index,e)
					index = index + len(e) + 1
			score = askForNumber("Score for "+player+":")
			newPoints = points - score
			
			if newPoints > 1:
				playerScores[player].append(score)
			elif newPoints < 0 or newPoints == 1:
				playerScores[player].append(0)
			elif newPoints  == 0:
				finished = True
				winner = player
				break
			displayBoard(players,playerScores,initPoints)
			screen.refresh()
	
	screen.refresh()
	clearLine(height-2)
	clearLine(height-3)
	winavg = sum(playerScores[winner]) / len(playerScores[winner])
	screen.addstr(height-1,0,winner+" has won with an average of %.2f! Press any key to exit." % winavg)
	screen.getkey()
	endCurses()
	
if __name__ == "__main__":
	main()
