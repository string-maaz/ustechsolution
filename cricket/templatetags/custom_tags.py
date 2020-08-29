from django import template
register = template.Library()



@register.filter(name='get_value')
def get_value(name,obj):
	return getattr(obj,name,'')

@register.filter(name='get_match_status')
def get_match_status(name,obj):
	return obj.get_match_status_display()


