from django.utils import timezone

"""
	@name: SupraOAth
	@author: exile.sas
	@date: 27/06/2016
	@licence: creative commons
"""
class SupraOAuth(object):
	def __call__(self, request):
		from models import OAuthToken
		if 'HTTP_AUTHORIZATION' in request.META:
			token = request.META['HTTP_AUTHORIZATION']
			token = OAuthToken.objects.filter(token=token).first()
			if token and token.enable and (token.expire_date == None or token.expire_date > timezone.now()):
				return None
			# end if
		# end if
		from django.core.exceptions import PermissionDenied
		raise PermissionDenied
	# end def
# end def
