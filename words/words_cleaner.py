def coroutine(func):
	def start(*args, **kwargs):
		cr = func(*args, **kwargs)
		cr.__next__()
		return cr
	return start

def hasNumbers(string):
	return any(i.isdigit() for i in string)

def hasNonLiterals(s, nonLiterals=['-', '.', ' ', '_', "'", '`']):
	return any(i in nonLiterals for i in s)

def hasUppers(s):
	return any(i.isupper() for i in s)


def wordLooper(word, score, prev, maxLength):
	if word == []:
		return False
	curLiteral = word.pop()
	score = score + 1 if curLiteral == prev else 1
	if score == maxLength:
		return True
	return wordLooper(word, score, curLiteral, maxLength)

def has3SameLiterals(s):
	return wordLooper(list(s), 0, '', 3)

def has2SameLiterals(s):
	return wordLooper(list(s), 0, '', 2)


@coroutine
def printer():
	while True:
		line = yield
		print(line)


def readerFile(filename, lim=None):
	with open(filename) as fin:
		for index, line in enumerate(fin):
			yield line
			if lim is not None and index == lim:
				break

@coroutine
def withoutDigit(target):
	while True:
		line = yield
		if not hasNumbers(line):
			target.send(line)

@coroutine
def without2SameLetters(target):
	while True:
		line = yield
		if not has2SameLiterals(line):
			target.send(line)

@coroutine
def isLongerThan3(target):
	while True:
		line = yield
		length = len(line)
		pipe = without2SameLetters(target)
		if length >= 3 and length <= 5:
			pipe.send(line)
		elif length > 5:
			target.send(line)


@coroutine
def without3SameLetters(target):
	while True:
		line = yield
		if not has3SameLiterals(line):
			target.send(line)


@coroutine
def withoutNonLiterals(target):
	while True:
		line = yield
		if not hasNonLiterals(line):
			target.send(line)

@coroutine
def withoutUppers(target):
	while True:
		line = yield
		if not hasUppers(line):
			target.send(line)

@coroutine
def fileCoroutine(filename):
    with open(filename, 'w') as fin:
        while True:
            line = yield
            fin.write(str(line) + '\n')

def main():
	prt = printer()
	fil = fileCoroutine('clean_words.txt')
	pipes = withoutDigit(isLongerThan3(withoutNonLiterals(withoutUppers(without3SameLetters(fil)))))
	# pipes = withoutNonLiterals(withoutDigit(isLongerThan3(prt)))
	for line in readerFile('words3.txt'):
		pipes.send(line.rstrip())


