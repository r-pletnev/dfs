def coroutine(func):
	def start(*args, **kwargs):
		cr = func(*args, **kwargs)
		cr.__next__()
		return cr
	return start

def filterPipe(func):
	def start(*args, **kwargs):
		print('args', args)
		print('kwargs', kwargs)
		return func(*args, **kwargs)
	return start

@filterPipe
def foo(bar, target='afsd'):
	pass

def hasNumbers(string):
	return any(i.isdigit()for i in string)

def hasNonLiteral(s, nonLiterals=['-', ' ', '_', "'", '`']):
	return any(i in nonLiterals for i in s)


@coroutine
def printer():
	while True:
		line = yield
		print(line)


def readerFile(filename, limit=20):
	with open(filename) as fin:
		for index, line in enumerate(fin):
			yield line
			if index == limit:
				break

@coroutine
def withoutDigit(target):
	while True:
		line = yield
		if not hasNumbers(line):
			target.send(line)

@coroutine
def isLongerThan3(target):
	while True:
		line = yield
		if len(line) >=3:
			target.send(line)

@coroutine
def withoutNonLiteras(target):
	while True:
		pass



def main():
	prt = printer()
	pipes = withoutDigit(isLongerThan3(prt))
	for line in readerFile('words3.txt', 40):
		pipes.send(line)


