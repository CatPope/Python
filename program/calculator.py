import math

print("숫자와 기호를 띄어 쓰시오")

def calculate(num1, sym, num2):
  if sym == '+':
    answer = num1+num2
  if sym == '-':
    answer = num1-num2
  if sym == '*':
    answer = num1*num2
  if sym == '/':
    answer = num1/num2
  if sym == '^':
    answer = num1**num2
  if sym == 'sqrt':
    answer = num1**(1/num2)
  return answer

while True:
  num1, sym, num2 = input().split()
  print(calculate(float(num1), sym, float(num2)))
