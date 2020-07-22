import json

from apscheduler.events import EVENT_JOB_ADDED, EVENT_JOB_SUBMITTED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler

from app.models.task_result import TaskResult, TaskState
from core.config import settings
from core.database import get_db


class Scheduler:
    # _scheduler = AsyncIOScheduler(settings.SCHEDULER)
    def __init__(self, ):
        self._scheduler = BackgroundScheduler(**settings.SCHEDULER)

    def init_app(self):
        self._scheduler.add_listener(callback=self.backend_result)
        return self._scheduler

    def backend_result(self, event):
        # db_session = get_db()
        if event.code & EVENT_JOB_ADDED:
            for db_session in get_db():
                _job = self._scheduler.get_job(event.job_id)
                result = TaskResult(
                    task_id=event.job_id,
                    task_name=_job.name,
                    task_args=str(_job.args),
                    task_kwargs=str(_job.kwargs),
                    status=TaskState.PENDING

                )
                db_session.add(result)
                db_session.commit()
        elif event.code & EVENT_JOB_SUBMITTED:
            for db_session in get_db():
                _job_result = db_session.query(TaskResult).filter_by(task_id=event.job_id).first()
                _job_result.status = TaskState.STARTED
                db_session.commit()

        elif event.code & EVENT_JOB_EXECUTED:
            for db_session in get_db():
                _job_result = db_session.query(TaskResult).filter_by(task_id=event.job_id).first()
                _job_result.status = TaskState.SUCCESS
                _job_result.result = json.dumps(event.retval)
                db_session.commit()
        elif event.code & EVENT_JOB_ERROR:
            for db_session in get_db():
                _job_result = db_session.query(TaskResult).filter_by(task_id=event.job_id).one()
                _job_result.status = TaskState.FAILURE
                _job_result.traceback = str(event.traceback)
                _job_result.exception = str(event.exception)
                db_session.commit()


scheduler = Scheduler().init_app()
