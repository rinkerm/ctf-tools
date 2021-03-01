import sys
import logging
import argparse
import gmpy2


def get_numeric_value(value):
	if(value.startswith("0x")):
		return int(value,16)
	else:
		return int(value)
def get_boolean_value(value):
	return bool(value)

def get_pq(n):
	if(n<=0):
		return n
	if(n%2==0):
		return (n/2,2)	
	x = gmpy2.isqrt(n)+1
	if(x*x==n):
		return (x,x)
	while(True):
		y_ = x* x -n
		if(y_>0):
			y = int(gmpy2.isqrt(y_))
			if(y*y==y_):
				return(x-y,x+y)
			else:
				x+=1

if __name__ == "__main__":
	logger = logging.getLogger("global_logger")
	parser = argparse.ArgumentParser(description="RSA With Bad e")
	parser._action_groups.pop()
	required = parser.add_argument_group("Required Arguments")
	optional = parser.add_argument_group("Optional Arguments")
	required.add_argument("-c", help="Specify the ciphertext. Format: Int or Hex")
	optional.add_argument("-p", help="Specify the first prime *NOTE: Either both p and q or n must be given* Format: Int or Hex")
	optional.add_argument("-q", help="Specify the second prime *NOTE: Either both p and q or n must be given* Format: Int or Hex")
	optional.add_argument("-n", help="Specify the modulus *NOTE: Either both p and q or n must be given* Format: Int or Hex")
	required.add_argument("-e", help="Specify the encryption exponent. Format: Int or Hex")
	optional.add_argument("-v", help="Verbose mode. Format: 0 = False, 1 = True")
	optional.add_argument("-o", help="Output mode. Format: 0 (default) = Hex, 1 = Int")
	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)


	# Default Values for Args
	p = 0
	q = 0
	e = 0
	n = 0
	c = 0
	v = False
	o = 0
	
	# Parse args if given	
	if args.v is not None:
		if(get_boolean_value(args.v) == 1):
			print("Analyzing Arguments")
			v = True
		else:
			v = False
	if args.o is not None:
		
		o = get_numeric_value(args.o)
		
		if(o>1):
			print("Error: Invalid o value")
			sys.exit(1)
		
		if(v):
			v_mode_output_text = ""
			if(o == 0):
				v_mode_output_text = "Hex"
			elif(o == 1):
				v_mode_output_text = "Integer"
			print("Output Mode: ",v_mode_output_text)
		
	p = 0
	q = 0
	e = 0
	n = 0
	c = 0	
	if args.p is not None:
		p = get_numeric_value(args.p)
		if(v):
			print("p: ",p)
			
	if args.q is not None:
		q = get_numeric_value(args.q)
		if(v):
			print("q: ",q)

	if args.n is not None:
		n = get_numeric_value(args.n)
		if(v):
			print("N: ",n)
	elif args.p is not None and args.q is not None:
		n = p*q
	else:
		print("Error: Cannot compute n value and no n value given")
		print("Please use either both -p and -q to give values to compute n or use -n")
		sys.exit(1)	
	if args.e is not None:
		e = get_numeric_value(args.e)
		if(v):
			print("e: ",e)
	if args.c is not None:
		c = get_numeric_value(args.c)
		if(v): 
			print("Cipher: ",c)
	if(v):
		print("Analyzing Complete, Checking e value")
		
	if ((p-1)%e==0 and (q-1)%e==0):
  		print ("Cannot recover. e is a factor of (p-1) and (q-1).")
  		sys.exit()
	if(v):
  		print("Calculating PHI")
  		
	if(p == 0 or q == 0):
  		if(v):
  			print("No p,q given, calculating p and q using fermet's factorization algorithm")
  		p,q = get_pq(n)
  	
	PHI = int( ((p-1)*(q-1) )//e)
  	
	if(v):
		print("PHI: ",PHI)
  	
  	#Recover d
  	
	if(v):
		print("Recovering d")
  	
	g = 1
	ge = 1
	while(ge==1):
		g=g+1
		ge = pow(g,PHI,n)
	if(v):
		print("GE: ",ge)
	d = gmpy2.invert(e,PHI)
	if(v):
		print("Recovered d")
		print("d: ",d)
		
	a = pow(c,d,n)
	
	l = 1 % n
	
	print("Plaintext Contenders:")
	
	for i in range(0,e-1):
		x = (a*l)%n
		if(o == 0):
			print(i,":","M: ",hex(x))
		elif(o == 1):
			print(i,":","M: ",x)
		l = (l*ge)%n

