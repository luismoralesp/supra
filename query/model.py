# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query import join

class relation(object):
	def __init__(self, model_name):
		self.model_name = model_name
	# end def

	def join(self, relation, on):
		return join(self, relation, on)
	# end def

	def as_sql(self):
		return self.model_name
	# end def
# end def

class classproperty(property):
	def __get__(self, cls, owner):
		return classmethod(self.fget).__get__(None, owner)()
	# end def
# end def

class model(relation):
	columns = None
	def __init__(self, model_name=None):
		super(model, self).__init__(model_name or type(self).__name__)
		for name in dir(self):
			if name != 'model':
				col = getattr(self, name)
				if isinstance(col, column):
					col.column_name = name
				# end if
		# end for
	# end def

	@classproperty
	def model(cls):
		if not cls.columns:
			cls.columns = cls()
		# end if
		return cls.columns
	# end def


	@staticmethod
	def column(column_name):
		return column(column_name)
	# end def

	def __call__(self, *params):
		params = map(str, params)
		return "%s(%s)" % (self.model_name, ', '.join(params))
	# end def

	def create_sql(self):
		columns = []
		for col in dir(self):
			if col != 'model':
				if isinstance(getattr(self, col), column):
					columns.append("%s %s" % (col, getattr(self, col).as_sql()))
				# end if
		# end for
		sql = "CREATE TABLE %(model_name)s (%(columns)s)" % {
			'model_name': self.model_name,
			'columns': ', '.join(columns)
		}
		return sql
	# end def
# end class

class column(object):
	def __init__(self, column_type):
		self.column_type = column_type
		self.column_name = None
		self.not_null = False
		self.unique = False
		self.pk = False
		self.fk = False
	# end def

	def not_null(self):
		self.not_null = True
	# end def

	def as_sql(self):
		return str(self.column_type)
	# end def
# end def

class constrain(object):
	def __init__(self, constrain_name, *columns):
		self.constrain_name = constrain_name
		self.columns = columns
		self.references = []
	# end def

	def references(self, *references):
		self.references = references
	# end def

	def as_sql(self):
		columns = []
		for column in self.columns:
			columns.append()
		# end for
		return "CONSTRAIN %(constrain_name)s %(columns)s%(references)s"
	# end def
# end class

		
	