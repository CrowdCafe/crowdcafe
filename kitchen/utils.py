from models import App, Job, QualityControl, Unit

def initJob(job):
	
	qualitycontrol, created = QualityControl.objects.get_or_create(job = job)