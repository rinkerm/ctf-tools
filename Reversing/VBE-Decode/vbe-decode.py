#!/usr/bin/env python3

__description__ = 'VBE Script Decoder'
__author__ = 'Matthew Rinker'
__version__ = '1.0'
__date__ = '2016/03/29'

import logging
import argparse
import sys
import os
import re

def str2bool(v):
	if isinstance(v,bool):
		return v
	if(v.lower() in ('yes','true','t','y','1')):
		return True
	elif(v.lower() in ('no','false','f','n','0')):
		return False
	else:
		raise argparse.ArgumentTypeError("V must be a boolean")

def file2str(i):
	try:
		infile = open(i,'r')
		data = infile.read()
		infile.close()
	except Exception as e:
		raise Exception(e)
	return data

def decode(data,v):

	decoded_bytes = ['\x57\x6E\x7B', '\x4A\x4C\x41', '\x0B\x0B\x0B', '\x0C\x0C\x0C', '\x4A\x4C\x41', '\x0E\x0E\x0E', '\x0F\x0F\x0F', '\x10\x10\x10', '\x11\x11\x11', '\x12\x12\x12', '\x13\x13\x13', '\x14\x14\x14', '\x15\x15\x15', '\x16\x16\x16', '\x17\x17\x17', '\x18\x18\x18', '\x19\x19\x19', '\x1A\x1A\x1A', '\x1B\x1B\x1B', '\x1C\x1C\x1C', '\x1D\x1D\x1D', '\x1E\x1E\x1E', '\x1F\x1F\x1F', '\x2E\x2D\x32', '\x47\x75\x30', '\x7A\x52\x21', '\x56\x60\x29', '\x42\x71\x5B', '\x6A\x5E\x38', '\x2F\x49\x33', '\x26\x5C\x3D', '\x49\x62\x58', '\x41\x7D\x3A', '\x34\x29\x35', '\x32\x36\x65', '\x5B\x20\x39', '\x76\x7C\x5C', '\x72\x7A\x56', '\x43\x7F\x73', '\x38\x6B\x66', '\x39\x63\x4E', '\x70\x33\x45', '\x45\x2B\x6B', '\x68\x68\x62', '\x71\x51\x59', '\x4F\x66\x78', '\x09\x76\x5E', '\x62\x31\x7D', '\x44\x64\x4A', '\x23\x54\x6D', '\x75\x43\x71', '\x4A\x4C\x41', '\x7E\x3A\x60', '\x4A\x4C\x41', '\x5E\x7E\x53', '\x40\x4C\x40', '\x77\x45\x42', '\x4A\x2C\x27', '\x61\x2A\x48', '\x5D\x74\x72', '\x22\x27\x75', '\x4B\x37\x31', '\x6F\x44\x37', '\x4E\x79\x4D', '\x3B\x59\x52', '\x4C\x2F\x22', '\x50\x6F\x54', '\x67\x26\x6A', '\x2A\x72\x47', '\x7D\x6A\x64', '\x74\x39\x2D', '\x54\x7B\x20', '\x2B\x3F\x7F', '\x2D\x38\x2E', '\x2C\x77\x4C', '\x30\x67\x5D', '\x6E\x53\x7E', '\x6B\x47\x6C', '\x66\x34\x6F', '\x35\x78\x79', '\x25\x5D\x74', '\x21\x30\x43', '\x64\x23\x26', '\x4D\x5A\x76', '\x52\x5B\x25', '\x63\x6C\x24', '\x3F\x48\x2B', '\x7B\x55\x28', '\x78\x70\x23', '\x29\x69\x41', '\x28\x2E\x34', '\x73\x4C\x09', '\x59\x21\x2A', '\x33\x24\x44', '\x7F\x4E\x3F', '\x6D\x50\x77', '\x55\x09\x3B', '\x53\x56\x55', '\x7C\x73\x69', '\x3A\x35\x61', '\x5F\x61\x63', '\x65\x4B\x50', '\x46\x58\x67', '\x58\x3B\x51', '\x31\x57\x49', '\x69\x22\x4F', '\x6C\x6D\x46', '\x5A\x4D\x68', '\x48\x25\x7C', '\x27\x28\x36', '\x5C\x46\x70', '\x3D\x4A\x6E', '\x24\x32\x7A', '\x79\x41\x2F', '\x37\x3D\x5F', '\x60\x5F\x4B', '\x51\x4F\x5A', '\x20\x42\x2C', '\x36\x65\x57']
	

	decoded_combination = [0, 1, 2, 0, 1, 2, 1, 2, 2, 1, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 0, 1, 2, 2, 1, 0, 2, 1, 2, 2, 1, 0, 0, 2, 1, 2, 1, 2, 0, 2, 0, 0, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0, 0, 1, 2, 2, 0, 0, 1, 2, 0, 2, 1]
	
	
	to_replace = ['@&','@#','@*','@!','@$']
	replace_with = [chr(10),chr(13),'>','<','@']

	decoded = ''
	if(v):
		print("Finding vbe markings")
	matches = list(re.findall(r'#@~\^......==(.+)......==\^#~@', data))

	if(len(matches)==0):
		raise Exception("No vbe markings found")

	if(v):
		print("Found {} sets of markings".format(len(matches)))

	j = 0
	for match in matches:
		if(v):
			print("Decoding match group: ", j)
		cur = match
		for i in range(0,5):
			cur = cur.replace(to_replace[i],replace_with[i])
		
		index = -1
		
		for char in cur:
			byte_val = ord(char)
			if(byte_val<128):
				index += 1
			
			if((byte_val == 9) or (byte_val > 31 and byte_val < 128) and (byte_val not in [60,62,64])): 
				possible_values = []
				for c in decoded_bytes[byte_val-9]:
					possible_values.append(c)
				decoded_char = possible_values[decoded_combination[index % 64]]
			else:
				decoded_char = char
			decoded += decoded_char
		
		decoded += '\n'
		j+=1

	return(decoded)
	

def main():
	if(args.i is not None):
		i = str(args.i)
	else:
		i = ''
		raise Exception("No input file given")
	if(args.o is not None):
		o = str(args.o)
	else:
		o = ''
	if(args.v is not None):
		v = str2bool(args.v)
	else:
		v = 0
	if(v):
		print("Verbose mode Enabled")
		
	if(v):
		print("Reading Input File")
	data = file2str(i)
	
	if(v):
		print("Decoding Data")
	decoded = decode(data,v)
	
	if(o == ''):
		sys.stdout.write(decoded)
	else:
		try:
			outfile = open(o,'w')
			outfile.write(decoded)
			print("Decoding Complete, exiting")
			outfile.close()
		except Exception as e:
			raise Exception(e)

if __name__ == '__main__':
	logger = logging.getLogger("global_logger")
	parser = argparse.ArgumentParser(description="VBE Decoder")
	parser._action_groups.pop()
	required = parser.add_argument_group("Required Arguments")
	optional = parser.add_argument_group("Optional Arguments")
	required.add_argument("-i", help="Specify the Input File. Format: Str")
	optional.add_argument("-v", help="Verbose mode. Format: Bln")
	optional.add_argument("-o", help="Output File. Format : Str")
	args = parser.parse_args()
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)
	main()
