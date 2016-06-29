from django import template
import json
register = template.Library()


@register.filter
def get_type(value):
	return type(value).__name__
#end def

@register.filter
def strip(dic):
	stri = json.dumps(dic)
	if len(stri) > 53:
		stri = stri[:50] + "..."
	#end if
	return stri
#end def