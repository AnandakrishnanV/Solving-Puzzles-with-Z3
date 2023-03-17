#!/usr/bin/env python2

import string
import random
from fractions import Fraction as frac
from secret import flag


def me(msg):
	if len(msg) == 1 :
		return ord(msg)
	msg = msg[::-1]
	reducer = len(msg) - 1
	resultNum, resultDen = frac(ord(msg[0]), reducer).denominator, frac(ord(msg[0]), reducer).numerator
	reducer -= 1
	for i in range(1, len(msg)-1):
		result =  ord(msg[i]) +  frac(resultNum, resultDen)
		resultDen, resultNum  = result.denominator, result.numerator
		resultDen, resultNum =  resultNum, reducer * resultDen
		reducer -= 1	
	result = ord(msg[-1]) + frac(resultNum, resultDen)
	resultDen, resultNum  = result.denominator, result.numerator
	return (resultNum, resultDen)

def you(msg):
	if len(msg) == 1 :
		return ord(msg)
	msg = msg[::-1]
	reducer = (-1) ** len(msg)
	result = frac(ord(msg[0]), reducer)
	resultNum, resultDen = result.denominator, result.numerator
	reducer *= -1
	for i in range(1, len(msg)-1):
		result =  ord(msg[i]) +  frac(resultNum, resultDen)
		resultDen, resultNum  = result.denominator, result.numerator
		resultDen, resultNum =  resultNum, reducer * resultDen
		reducer *= -1

	result = ord(msg[-1]) + frac(resultNum, resultDen)
	resultDen, resultNum  = result.denominator, result.numerator
	return (resultNum, resultDen)

def us(msg):
	if len(msg) == 1 :
		return ord(msg)
	msg = msg[::-1]
	reducer = (-1) ** int(frac(len(msg), len(msg)**2))
	result = frac(ord(msg[0]), reducer)
	resultNum, resultDen = result.denominator, result.numerator
	reducer **= -1
	reducer = int(reducer)
	for i in range(1, len(msg)-1):
		result =  ord(msg[i]) +  frac(resultNum, resultDen)
		resultDen, resultNum  = result.denominator, result.numerator
		resultDen, resultNum =  resultNum, reducer * resultDen
		reducer **= -1
		reducer = int(reducer)
	result = ord(msg[-1]) + frac(resultNum, resultDen)
	resultDen, resultNum  = result.denominator, result.numerator
	return (resultNum, resultDen)

dict_encrypt = {
	1: me,
	2: you,
	3: us,
	4: you,
	5: me
}
cipher = [[] for _ in range(5)]
S = list(range(1,6))
random.shuffle(S)
print("enc = [")
for i in range(4):
	cipher[i] = dict_encrypt[S[i]](flag[int(i * len(flag) // 5) : int(i * len(flag) // 5 + len(flag) // 5)])
	print(cipher[i])
	print(", ")
i += 1
cipher[i] = dict_encrypt[S[i]](flag[int(i * len(flag) // 5) : int(i * len(flag) // 5 + len(flag) // 5)])
print(cipher[i])
print( " ]")

