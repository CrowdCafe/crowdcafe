from django import template
from django.template import Context, Template
register = template.Library()
from kitchen.models import Job

def include_external(context,job_id):
	job = Job.objects.filter(pk = job_id).get()

	html = job.userinterface_html
	t = Template(html)
	return t.render(context)

def render_instructions(context,job_id):
	job = Job.objects.filter(pk = job_id).get()

	html = job.description
	t = Template(html)
	return t.render(context)

register.simple_tag(takes_context=True)(include_external)
register.simple_tag(takes_context=True)(render_instructions)