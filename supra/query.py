# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class sentence(object):
	def __init__(self, sentence, context):
		self.sentence = sentence
		self.context = context
	# end def

	def as_sql(self):
		sql = ""
		for i in range(self.context.tabulation):
			sql = sql + "    "
		# end for
		sql = sql + self.sentence.as_sql()
		return sql
	# end def
# end class

class context(object):

	def __init__(self):
		self.declares = []
		self.sentences = []
		self.ctx = None
	# end def

	@property
	def tabulation(self):
		ctx = self
		tabulation = 0
		while (ctx):
			ctx = ctx.ctx
			tabulation = tabulation + 1
		# end def
		return tabulation
	# end def

	def do(self, *sentences):
		for sentence in sentences:
			self.append(sentence)
		# end if
		return self
	# end def

	def append(self, sentence):
		sentence.ctx = self
		self.sentences.append(sentence)
		return self
	# end def

	def as_sql(self):
		sql = ""
		for declare in self.declares:
			sql = sql + sentence(declare, self).as_sql() + ";\n"
		# end for
		for sent in self.sentences:
			sql = sql + sentence(sent, self).as_sql() + ";\n"
		# end for
		return sql
	# end def
# end class

body = context()

class set():
	def __init__(self, var_name, value):
		self.var_name = var_name
		self.value = value
	# end def

	def as_sql(self):
		return "%(var_name)s := %(value)s" % {
			"var_name": self.var_name,
			"value": self.value,
		}
	# end def
# end class

class operation(object):
	def __init__(self, var_name1, operator, var_name2):
		self.var_name1 = var_name1
		self.operator = operator
		self.var_name2 = var_name2
	# end def
	def as_sql(self):
		return "(%(var_name1)s %(operator)s %(var_name2)s)" % {
			"var_name1": self.var_name1,
			"operator": self.operator,
			"var_name2": self.var_name2,
		}
	# end def

	def by(self, value):
		return operation(self, "*", value)
	# end def

	def div(self, value):
		return operation(self, "/", value)
	# end def

	def plus(self, value):
		return operation(self, "+", value)
	# end def

	def minus(self, value):
		return operation(self, "-", value)
	# end def

	def o(self, value):
		return operation(self, "or", value)
	# end def

	def y(self, value):
		return operation(self, "and", value)
	# end def

	def eq(self, value):
		return operation(self, "=", value)
	# end def

	def dis(self, value):
		return operation(self, "<>", value)
	# end def

	def gt(self, value):
		return operation(self, ">", value)
	# end def

	def lt(self, value):
		return operation(self, "<", value)
	# end def

	def gte(self, value):
		return operation(self, ">=", value)
	# end def

	def lte(self, value):
		return operation(self, "<=", value)
	# end def

	def __unicode__(self):
		return self.as_sql()
	# end def
# end class

class comparation(operation):
	pass
# end class

class close(object):
	def __init__(self, closing):
		self.closing = closing
	# end def

	def as_sql(self):
		return "end %s" % (self.closing, )
	# end if
# end class

class for_loop(context):
	def __init__(self, var_name, start, end, step=1):
		super(for_loop, self).__init__()
		self.var_name = var_name
		self.start = start
		self.end = end
		self.step = step
	# end def

	def as_sql(self):
		sql = "for %(var_name)s = %(start)s to %(end)s loop\n" % {
			"var_name": self.var_name,
			"start": self.start,
			"end": self.end,
			"step": self.step,
		}
		sql = sql + super(for_loop, self).as_sql()
		sql = sql + sentence(close("loop"), self.ctx).as_sql()
		return sql
	# end def
# end class

class for_in(context):
	def __init__(self, var_name, inn):
		super(for_in, self).__init__()
		self.var_name = var_name
		self.inn = inn
	# end def

	def as_sql(self):
		sql = "for %(var_name)s in (%(inn)s) loop\n" % {
			"var_name": self.var_name,
			"inn": self.inn,
		}
		sql = sql + super(for_in, self).as_sql()
		sql = sql + sentence(close("loop"), self.ctx).as_sql()
		return sql
	# end def
# end class

class declare(operation):
	def __init__(self, var_name, var_type, default_value=None):
		self.var_name = var_name
		self.var_type = var_type
		self.default_value = default_value or 'null'
		body.declares.append(self)
	# end def

	def as_sql(self):
		return "declare %(var_name)s as %(var_type)s := %(default_value)s" % {
			"var_name": self.var_name,
			"var_type": self.var_type,
			"default_value": self.default_value,
		}
	# end def

	def __unicode__(self):
		return self.var_name
	# end def

	def set(self, value):
		return set(var_name=self.var_name, value=value)
	# end def
# end class

class select(object):
	def __init__(self, *selects):
		self.selects = selects
		self.comparations = []
		self.group_bys = []
	# end def

	def from_models(self, *models):
		self.models = models
		return self
	# end def

	def where(self, *comparations):
		self.comparations = comparations
		return self
	# end def

	def group_by(self, *group_bys):
		self.group_bys = group_bys
		return self
	# end def

	def limit(self, *limits):
		self.limits = limits
		return self
	# end def

	def as_sql(self):
		selects = []
		for select in self.selects:
			selects.append(select.as_sql())
		# end for
		models = []
		for model in self.models:
			models.append(model.as_sql())
		# end for
		comparations = []
		for comparation in self.comparations:
			comparations.append(comparation.as_sql())
		# end for
		limits = []
		for limit in self.limits:
			limits.append(str(limit))
		# end for
		group_bys = []
		for group_by in self.group_bys:
			group_bys.append(group_by.as_sql())
		# end for
		if len(comparations):
			comparations = " WHERE " + ', '.join(comparations)
		else:
			comparations = ""
		# end if
		if len(group_bys):
			group_bys = " GROUP BY " + ', '.join(group_bys)
		else:
			group_bys = ""
		# end if
		if len(limits):
			limits = " LIMIT " + ', '.join(limits)
		else:
			limits = ""
		# end if
		sql = "SELECT %(selects)s FROM %(models)s%(comparations)s%(group_bys)s%(limits)s" % {
			"selects": ', '.join(selects),
			"models": ', '.join(models),
			"comparations": comparations,
			"group_bys": group_bys,
			"limits": limits,
		}
		return sql
	# end def
# end class

class column(object):
	def __init__(self, column_name):
		self.column_name = column_name
	# end def

	def as_sql(self):
		return self.column_name
	# end def
# end def

class relation(object):
	def __init__(self, model_name):
		self.__model_name = __model_name__
	# end def

	def cols(self, *columns):
		for col in columns:
			setattr(self, col, column(col))
		# end for
		return self
	# end def

	def join(self, relation, on):
		return join(self, relation, on)
	# end def

	def as_sql(self):
		return self.__model_name__
	# end def
# end def

class model(relation):
	def __init__(self, model_name):
		super(model, self).__init__(model_name)
	# end def

	def __setattr__(self, attr):
		print attr
	# end def
# end class

class join(object):
	def __init__(self, relation1, relation2, on):
		self.relation1 = relation1
		self.relation2 = relation2
		self.on = on
	# end def

	def as_sql(self):
		sql = "%(relation1)s JOIN %(relation2)s ON %(on)s" % {
			"relation1": self.relation1.as_sql(),
			"relation2": self.relation2.as_sql(),
			"on": self.on.as_sql(),
		}
		return sql
	# end def
# end class

class aggregation(object):
	def __init__(self, aggregation_name, *params):
		self.aggregation_name = aggregation_name
		self.params = params
	# end def

	def as_sql(self):
		params = []
		for param in self.params:
			params.append(param.as_sql())
		# end for
		sql = "%(aggregation_name)s(%(params)s)" % {
			"aggregation_name": self.aggregation_name,
			"params": ', '.join(params)
		}
		return sql
# end class

class sum_agg(aggregation):
	def __init__(self, *params):
		super(sum_agg, self).__init__("sum", *params)
	# end def
# end class

class count_agg(aggregation):
	def __init__(self, *params):
		super(count_agg, self).__init__("count", *params)
	# end def
# end class