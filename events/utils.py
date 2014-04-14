from models import Event
from django.core.urlresolvers import resolve

def logEvent(request, page, parent_id = None, object_id = None):
    event = Event(
        page = page,
        url = resolve(request.path_info).url_name
        )

    if 'cafe-context' in request.session:
        event.context = request.session['cafe-context']
    if request.user.is_authenticated():
        event.user = request.user

    if parent_id:
        event.parent_id = parent_id
    if object_id:
        event.object_id = object_id
    
    event.save()