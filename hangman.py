import random

words = []

def init():
	f = open("hangman_words.txt", "r")
	global words
	words = f.read().split()
	f.close()

def choose_word():
	return random.choice(words)