#!/usr/bin/env python2
import os
with open ('./file/680VBFhpBNBJOYXebSxgwLrtbh3g6JFUllqksWFSsGshhwsguyNL26MGul2oZ3b8' , 'rb') as f:
	data = f.read()
	#print (data)
	xor_data = 'adR2b4nh'
	len_x = os.path.getsize('./file/680VBFhpBNBJOYXebSxgwLrtbh3g6JFUllqksWFSsGshhwsguyNL26MGul2oZ3b8')
	print len_x
	len_d = len(xor_data)
	save=''
	for i in range(84705):
		print i
		save+=(chr(ord(data[i]) ^ ord(xor_data[i%len_d])))
	with open('new_hex_data' , 'wb') as f2:
		f2.write(save)