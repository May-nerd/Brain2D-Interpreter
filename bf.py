from collections import defaultdict, Counter
import sys



valid = "><^v+-,.[]"

def parse(brainFuck):
	leftCounter = rightCounter = 0
	brackets = {}
	parsedInput = ''.join([char for char in brainFuck if char in valid])
	for key,char in enumerate(parsedInput):
		if char == "[":
			leftCounter += 1
			rightCounter = leftCounter
			brackets[key] = leftCounter
		elif char == "]":
			while rightCounter in [x for x, y in Counter(brackets.values()).items() if y > 1]:
				rightCounter -= 1
			brackets[key] = rightCounter
	bracketList = defaultdict(list)
	for k, v in brackets.items():
		bracketList[v].append(k)
	bracketList =  list(dict(bracketList).values())
	# for subList in bracketList:
	# 	subList.sort()
	return parsedInput, bracketList

def main(args):
	parsedInput = args[0]
	brackets = args[1]
	print(parsedInput)
	print(brackets)
	counter = tapeCounterX = tapeCounterY = 0
	cols_count = 3000
	rows_count = 3000
	tape = [[0 for x in range(cols_count)] for x in range(rows_count)] 
	while counter < len(parsedInput):
		char = parsedInput[counter]
		if char == ">":
			tapeCounterX +=1
		elif char == "<":
			tapeCounterX -=1
		elif char == "^":
			tapeCounterY -=1
		elif char == "v":
			tapeCounterY +=1
		elif char == "+":
			tape[tapeCounterX][tapeCounterY] += 1
		elif char == "-":
			tape[tapeCounterX][tapeCounterY] -= 1
		elif char == ",":
			tape[tapeCounterX][tapeCounterY] = ord(input("Enter: ")[0])
		elif char == ".":
			print(chr(tape[tapeCounterX][tapeCounterY]), end='')
		elif char == "[" and tape[tapeCounterX][tapeCounterY] == 0:		
			key = [y[0] for y in brackets].index(counter)
			counter = brackets[key][1]
			continue
		elif char == "]" and tape[tapeCounterX][tapeCounterY] != 0:
			key = [y[1] for y in brackets].index(counter)
			counter = brackets[key][0]
			continue
		counter+=1




with open('hello.b2d', 'r') as myfile:
  code=myfile.read()

main(parse(code))
