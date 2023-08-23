from Crypto.Util.number import bytes_to_long, getPrime

flag = open('flag','r').read().strip().encode()
flag = bytes_to_long(flag)

n = 1
output = open('output','w')
while n < flag:
	p = getPrime(64)
	output.write('%d,%d\n' % (flag % p, p))
	n *= p
output.close()
