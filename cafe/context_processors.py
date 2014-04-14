from django.conf import settings

#this for having userProfile always in the session
#this is called before rendering the template, so forget about the session.
def task_categories(request):
    try:
    	categories = []
    	for key in settings.TASK_CATEGORIES.keys():
    		categories.append(settings.TASK_CATEGORIES[key])
        return {'task_categories':reversed(categories)}    
    except:
        return {}