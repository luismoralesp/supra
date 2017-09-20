# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class sqltype(object):
	def __init__(self, type_name):
		self.type_name = type_name
	# end def

	def __call__(self, *params):
		params = map(str, params)
		return "%s(%s)" % (self.type_name, ', '.join(params))
	# end def

	def __str__(self):
		return self.type_name
	# end def
# end def

bigint = sqltype("BIGINT")
bigserial = sqltype("BIGSERIAL")
boolean = sqltype("BOOLEAN")
byte = sqltype("BYTE")
char = sqltype("CHAR")
character = sqltype("CHARACTER")
character = sqltype("CHARACTER VARYING") 
date = sqltype("DATE")
datetime = sqltype("DATETIME")
dec = sqltype("DEC")
decimal = sqltype("DECIMAL")
double = sqltype("DOUBLE PRECISION") 
floating = sqltype("FLOAT")
idssecuritylabel = sqltype("IDSSECURITYLABEL")
integer = sqltype("INTEGER")
int8 = sqltype("INT8")
interval = sqltype("INTERVAL")
lvarchar = sqltype("LVARCHAR")
money = sqltype("MONEY")
numeric = sqltype("NUMERIC")
real = sqltype("REAL")
serial = sqltype("SERIAL")
serial8 = sqltype("SERIAL8")
smallfloat = sqltype("SMALLFLOAT")
smallint = sqltype("SMALLINT")
text = sqltype("TEXT")
varchar = sqltype("VARCHAR")
