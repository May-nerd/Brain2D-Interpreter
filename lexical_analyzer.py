# For this problem we do *not* care about line number information. Only the types and values of tokens matter. Whitespace characters are ' \t\v\r' (and we have already filled them in for you below). 

# Complete the lexer below. 
import ply.lex as lex

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'IDENT', 'STRING', 'NUMBER') 

####

# Place your token definition rules here.

def t_NUMBER(t):
	r'(\d)(\d|_)*'
	t.value = int(t.value.replace("_", ""))
	return t

def t_STRING(t):
  r'(\".*?\")|(\'.*?\')'
  t.value = t.value.replace("\'", "'")
  return t

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_IDENT = r'[A-Za-z][A-Za-z_]*'




####
t_ignore = ' \t\v\r'

def t_error(t):
  print ("Lexer: unexpected character " + t.value[0])
  t.lexer.skip(1)

# We have included some testing code to help you check your work. 

lexer = lex.lex() 

def test_lexer(input_string):
  lexer.input(input_string)
  result = [ ] 
  while True:
      tok = lexer.token()
      if not tok: break
      result = result + [(tok.type,tok.value)]
  return result

#Output:
question1 = " +   -   /   * " 
print("QUESTION1: " + question1)
answer1 = [('PLUS', '+'), ('MINUS', '-'), ('DIVIDE', '/'), ('TIMES', '*')]
print(test_lexer(question1));
print (test_lexer(question1) == answer1)

question2 = """ 'string "nested" \' "inverse 'nested'" """
answer2 = [('STRING', 'string "nested" '), ('STRING', "inverse 'nested'")]
print("\nQUESTION2: " + question2 + "")
print(test_lexer(question2));
print (test_lexer(question2) == answer2) 

question3 = """ 12_34 5_6_7_8 0______1 1234 """
answer3 = [('NUMBER', 1234), ('NUMBER', 5678), ('NUMBER', 1), ('NUMBER', 1234)]
print("\nQUESTION3: " + question3+ "")
print(test_lexer(question3));
print (test_lexer(question3) == answer3)

question4 = """ 'he'llo w0rld 33k """
answer4 = [('STRING', 'he'), ('IDENT', 'llo'), ('IDENT', 'w'), ('NUMBER',
0), ('IDENT', 'rld'), ('NUMBER', 33), ('IDENT', 'k')]
print("\nQUESTION4: " + question4 + "")
print(test_lexer(question4));
print (test_lexer(question4) == answer4)
