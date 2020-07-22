from core.database import Base
import sqlalchemy as sa
from sqlalchemy_utils.types.choice import ChoiceType
import enum
from datetime import datetime


class TaskState(enum.Enum):
    #: Task state is unknown (assumed pending since you know the id).
    PENDING = 'PENDING'
    #: Task was started by a worker (:setting:`task_track_started`).
    STARTED = 'STARTED'
    #: Task succeeded
    SUCCESS = 'SUCCESS'
    #: Task failed
    FAILURE = 'FAILURE'
    #: Task was revoked.
    REVOKED = 'REVOKED'
    #: Task was rejected (only used in events).
    REJECTED = 'REJECTED'
    #: Task is waiting for retry.
    RETRY = 'RETRY'
    IGNORED = 'IGNORED'

    def __str__(self):
        return self.value


class TaskResult(Base):
    __tablename__ = 'task_result'
    id = sa.Column(sa.Integer, comment='id', primary_key=True)
    task_id = sa.Column(sa.String(255), unique=True, comment="task id")
    task_name = sa.Column(sa.String(255), comment='task名称')
    task_args = sa.Column(sa.TEXT, nullable=True)
    task_kwargs = sa.Column(sa.TEXT, nullable=True)
    status = sa.Column(ChoiceType(TaskState), default=TaskState.PENDING, comment='任务状态')
    result = sa.Column(sa.TEXT, default=None, nullable=True, comment='执行结果')
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, comment='任务开始时间')
    updated_at = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow,
                           comment='任务结束时间')
    traceback = sa.Column(sa.TEXT, nullable=True, default=None, comment='异常详情')
    exception = sa.Column(sa.TEXT, nullable=True, default=None, comment='异常原因')
