from django import template
from django.template import Context, Template
register = template.Library()
from kitchen.models import Task

def include_external(context,task_id):
	task = Task.objects.filter(pk = task_id).get()

	html = task.template_html
	t = Template(html)
	return t.render(context)

register.simple_tag(takes_context=True)(include_external)