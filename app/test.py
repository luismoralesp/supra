# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query.model import model
from query.query import *
from query.sentence import *
from query.types import *

class Tabla(model):
	column1 = model.column(integer)
	column2 = model.column(varchar(45))
# end class

a = declare("a", integer)
body.do(
	a.set(a.plus(1)),
	for_loop(a, 1, 10).do(
		a.set(a.by(2))
	),
	for_in(a, select(Tabla.model.column1).from_models(Tabla.model).where())
)


print body.as_sql()

print Tabla().create_sql()