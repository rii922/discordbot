import copy
import random

def is_winning_hand(hand, meld=4, eye=1):
	if meld == 0 and eye == 0:
		return True
	if meld > 0:
		for i in range(9):
			if hand[i] >= 3:
				nhand = copy.copy(hand)
				nhand[i] -= 3
				if is_winning_hand(nhand, meld-1, eye):
					return True
		for i in range(7):
			if hand[i] >= 1 and hand[i+1] >= 1 and hand[i+2] >= 1:
				nhand = copy.copy(hand)
				nhand[i] -= 1
				nhand[i+1] -= 1
				nhand[i+2] -= 1
				if is_winning_hand(nhand, meld-1, eye):
					return True
	if eye > 0:
		for i in range(9):
			if hand[i] >= 2:
				nhand = copy.copy(hand)
				nhand[i] -= 2
				if is_winning_hand(nhand, meld, eye-1):
					return True
	return False

def add_random_chow(hand):
	chow_list = []
	for i in range(7):
		if hand[i] <= 3 and hand[i+1] <= 3 and hand[i+2] <= 3:
			chow_list.append(i)
	chow_begin = random.choice(chow_list)
	for i in range(3):
		hand[chow_begin+i] += 1

def add_random_pong(hand):
	pong_list = []
	for i in range(9):
		if hand[i] <= 1:
			pong_list.append(i)
	pong = random.choice(pong_list)
	hand[pong] += 3

def add_random_eye(hand):
	eye_list = []
	for i in range(9):
		if hand[i] <= 2:
			eye_list.append(i)
	eye = random.choice(eye_list)
	hand[eye] += 2

def generate_quiz():
	hand = [0 for _ in range(9)]
	for _ in range(4):
		if random.randrange(4) == 0:
			add_random_pong(hand)
		else:
			add_random_chow(hand)
	add_random_eye(hand)
	eliminate_list = []
	for i in range(9):
		if hand[i] > 0:
			eliminate_list.append(i)
	hand[random.choice(eliminate_list)] -= 1
	ans = set()
	for i in range(9):
		if hand[i] <= 3:
			nhand = copy.copy(hand)
			nhand[i] += 1
			if is_winning_hand(nhand):
				ans.add(i)
	return (hand, ans)