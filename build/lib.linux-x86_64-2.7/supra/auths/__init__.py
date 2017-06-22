from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import Resolver404


"""
	@name: SupraAuthenticationMixin
	@author: exile.sas
	@date: 27/06/2016
	@licence: creative commons
"""
class SupraAuthenticationMixin(object):
	auths = []

	def auth(self, request, *args, **kwargs):
		for auth in self.auths:
			au = auth()(request)
			if au:
				return au
			# end if
		# end for
	# end def

	@classmethod
	def append(cls, method):
		cls.auths.append(method)
	# end def

# end class

methods = SupraAuthenticationMixin