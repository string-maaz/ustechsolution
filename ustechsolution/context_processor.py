def get_cancel_url(request):
	from django.core.urlresolvers import reverse_lazy
	request_data = request.META
	referer = request_data.get('HTTP_REFERER')
	current_url = request_data.get('HTTP_HOST') + request_data.get('PATH_INFO')
	return {'HTTP_REFERER': reverse_lazy('dashboard') if not referer or referer == current_url else referer }