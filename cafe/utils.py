



'''
def generateTask(job,user):

    score = job.qualitycontrol.score(user)
    if job.qualitycontrol.allowed_to_work_more(user):
        dataitems_regular = availableDataItems(job, user, False)
        dataitems_gold = availableDataItems(job, user, True)
        
        
        if score > job.qualitycontrol.gold_max:
            gold_amount_to_put = 0
        if score > job.qualitycontrol.gold_min and score <= job.qualitycontrol.gold_max:
            gold_amount_to_put = max([score - job.qualitycontrol.gold_min,job.qualitycontrol.gold_min])
        if score <= job.qualitycontrol.gold_min:
            gold_amount_to_put = job.qualitycontrol.gold_max

        dataitems_to_put = []
        if dataitems_regular:
            gold_amount_to_put = 0
            regular_amount_to_put = 0
            if dataitems_gold:
                if score > job.qualitycontrol.gold_max:
                    gold_amount_to_put = job.qualitycontrol.gold_min
                if score > job.qualitycontrol.gold_min and score <= job.qualitycontrol.gold_max:
                    gold_amount_to_put = max([job.qualitycontrol.gold_max - score,job.qualitycontrol.gold_min])
                if score <= job.qualitycontrol.gold_min:
                    gold_amount_to_put = job.qualitycontrol.gold_max

                gold_amount_to_put = min([dataitems_gold.count(), int(gold_amount_to_put)])
                dataitems_to_put = random.sample(dataitems_gold.all(), gold_amount_to_put) 

            regular_amount_to_put = min([dataitems_regular.count(),int(job.qualitycontrol.dataitems_per_task - gold_amount_to_put)]) 
            dataitems_to_put += random.sample(dataitems_regular.all(), regular_amount_to_put)
            shuffle(dataitems_to_put)
            
            task = Task(job=job)
            task.save()
            task.dataitems.add(*dataitems_to_put)
            task.save()
            return task
    return False

def userIsQualifiedForJob(job,user, mobile):
    if availableDataItems(job, user) and job.qualitycontrol.allowed_to_work_more(user) and qualifiedJob(job,user) and (job.qualitycontrol.device_type == 0 or (mobile and job.qualitycontrol.device_type == 1) or (not mobile and job.qualitycontrol.device_type == 2)):
        return True
    else:
        return False

def availableDataItems(job, user, gold = False):

    dataitems_already_did = AnswerItem.objects.filter(answer__executor = user, dataitem__job = job).values('dataitem')
    dataitems_available = DataItem.objects.filter(job = job, status = 'NR', gold = gold).exclude(pk__in = dataitems_already_did)

    if dataitems_available.count()>0:
        return dataitems_available
    else:
        return False
'''