# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class select(object):
	def __init__(self, *selects):
		self.selects = selects
		self.comparations = []
		self.group_bys = []
		self.models = []
		self.limits = []
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
			selects.append(select.column_name)
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
		if len(models):
			models = " FROM " + ', '.join(models)
		else:
			models = ""
		# end if
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
		sql = "SELECT %(selects)s%(models)s%(comparations)s%(group_bys)s%(limits)s" % {
			"selects": ', '.join(selects),
			"models": models,
			"comparations": comparations,
			"group_bys": group_bys,
			"limits": limits,
		}
		return sql
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