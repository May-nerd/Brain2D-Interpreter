import ply.lex as lex
import sys

# Helper class stack
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class _Getch:
   """Gets a single character from standard input.  Does not echo to the
screen."""
   def __init__(self):
       try:
           self.impl = _GetchWindows()
       except ImportError:
           self.impl = _GetchUnix()

   def __call__(self): return self.impl()


class _GetchUnix:
   def __init__(self):
       import tty, sys

   def __call__(self):
       import sys, tty, termios
       fd = sys.stdin.fileno()
       old_settings = termios.tcgetattr(fd)
       try:
           tty.setraw(sys.stdin.fileno())
           ch = sys.stdin.read(1)
       finally:
           termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
       return ch


class _GetchWindows:
   def __init__(self):
       import msvcrt

   def __call__(self):
       import msvcrt
       return msvcrt.getch()


getch = _Getch()

# LEXER
tokens = ('PLUS', 'MINUS', 'LEFT', 'RIGHT', 'OUTPUT', 'INPUT', 'LBRACKET', 'RBRACKET', 'NEWLINE') 

t_PLUS = r'\+'
t_MINUS = r'-'
t_LEFT = r'<'
t_RIGHT = r'>'
t_OUTPUT = r'\.'
t_INPUT = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_NEWLINE = r'\n'

t_ignore = ' \t\v\r'

def t_error(t):
  print ("Comment character: " + t.value[0])
  t.lexer.skip(1)

lexer = lex.lex() 


# Parser
def bf_parser(input_string):
  lexer.input(input_string)
  result = [ ] 
  stack = Stack()
  brackets = []
  indexCounter = 0
  lineNum = 1
  lBracketLineNum = Stack()
  error_msg = ""
  while True:
      tok = lexer.token()
      
      if not tok: 
        break
      
      if(tok.type == "NEWLINE"):
        lineNum += 1
        continue
      else:
        result = result + [(tok.type,tok.value)]
      
      if(tok.type == "LBRACKET"):
        stack.push(indexCounter)
        lBracketLineNum.push(lineNum)
      elif(tok.type == "RBRACKET"):
        if stack.isEmpty():
          error_msg = "Syntax Error: Unmatched right bracket at line " + str(lineNum) +  "."
          return None, error_msg  
        lBracketLineNum.pop()
        lBracketIndex = stack.pop()
        rBracketIndex = indexCounter
        brackets.append([lBracketIndex, rBracketIndex])
      indexCounter+=1
    

  # IF STACK IS STILL THERE
  if(not(stack.isEmpty())):
    while not(stack.isEmpty()):
      stack.pop()
      error_msg += "Syntax Error: Unmatched left bracket at line " + str(lBracketLineNum.pop()) +  ".\n"
    return None, error_msg

  return result, brackets

def execute(args):
  if(args[0] == None):
    print(args[1])
    return 0
  parsedInput = args[0]
  brackets = args[1]
  # print(parsedInput)
  # print(brackets)
  counter = tapeCounterX = tapeCounterY = 0
  cols_count = 3000
  rows_count = 3000
  tape = [[0 for x in range(cols_count)] for x in range(rows_count)] 
  while counter < len(parsedInput):
    # 0 is the token
    # 1 is the lexeme
    char = parsedInput[counter][1]
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
      tape[tapeCounterX][tapeCounterY] = ord(input()[0])
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


# Main program
if(len(sys.argv) < 2):
  print("Brain2D Interpreter: No file to interpret");
else:
  with open(sys.argv[1], 'r') as myfile:
    code=myfile.read()

  execute(bf_parser(code))



