#!/usr/bin/env python

import socket
import struct
import cgi
import cgitb; cgitb.enable()

PROTO_BASE = 0

CUTOAN_CHART = (PROTO_BASE+504)
ANTOCU_CHART = (PROTO_BASE+505)

fields = cgi.FieldStorage()

if fields.has_key("host"):
	host = fields.getvalue("host")
else:
	host = ''
if fields.has_key("port"):
	try:
		port = int(fields.getvalue("port"))
	except ValueError:
		port = 0
else:
	port = 0
if fields.has_key("id"):
	try:
		chartid = int(fields.getvalue("id"))
	except ValueError:
		chartid = -1
else:
	chartid = -1

def mysend(socket,msg):
	totalsent = 0
	while totalsent < len(msg):
		sent = socket.send(msg[totalsent:])
		if sent == 0:
			raise RuntimeError, "socket connection broken"
		totalsent = totalsent + sent

def myrecv(socket,leng):
	msg = ''
	while len(msg) < leng:
		chunk = socket.recv(leng-len(msg))
		if chunk == '':
			raise RuntimeError, "socket connection broken"
		msg = msg + chunk
	return msg

if host=='' or port==0 or chartid<0:
	print "Content-Type: image/gif"
	print
	f = open('err.gif')
	print f.read(),
	f.close()
else:
	try:
		s = socket.socket()
		s.connect((host,port))
		mysend(s,struct.pack(">LLL",CUTOAN_CHART,4,chartid))
		header = myrecv(s,8)
		cmd,length = struct.unpack(">LL",header)
		if cmd==ANTOCU_CHART and length>0:
			data = myrecv(s,length)
#		data = s.recv(length)
#		print len(data),length
			if data[:3]=="GIF":
				print "Content-Type: image/gif"
				print
				print data,
			elif data[:8]=="\x89PNG\x0d\x0a\x1a\x0a":
				print "Content-Type: image/png"
				print
				print data,
			else:
				print "Content-Type: image/gif"
				print
				f = open('err.gif')
				print f.read(),
				f.close()
		else:
			print "Content-Type: image/gif"
			print
			f = open('err.gif')
			print f.read(),
			f.close()
		s.close()
	except Exception:
		print "Content-Type: image/gif"
		print
		f = open('err.gif')
		print f.read(),
		f.close()
