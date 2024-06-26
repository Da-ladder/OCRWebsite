from django.conf import settings
import django
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if settings.configured:
    pass
else:
    settings.configure(DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    })
    django.setup()



from celery import Celery, shared_task
from celery.contrib.abortable import AbortableTask

try:
    from webFuncts.wrapper import *
    pass
except:
    from .webFuncts.wrapper import *
    pass




# if debugging use """, backend="rpc://"  """
app = Celery('tasks',broker='amqp://guest:guest@localhost:5672//')

#app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


#bind=True allows you to access self, not needed bc static functions
@shared_task(name="websiteFace.task.addVid_async", base=AbortableTask)
def addVid_async(lin):
    VideoProcesser.addVideo(lin)
    pass

@shared_task(name="websiteFace.task.findTeam_async", base=AbortableTask)
def findTeam_async(lin, tea):
    ImageProcesser.findTeam(lin, tea)
    pass