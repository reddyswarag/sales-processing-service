from sqlalchemy import Text, Identity,Integer,DateTime
from sqlalchemy.orm import mapped_column, Mapped
from database import Base,engine
from sqlalchemy.dialects.postgresql import JSONB
import datetime 

class Job(Base):

    __tablename__ = "jobs"

    job_id : Mapped[int] = mapped_column(
        Identity(always = True),
        primary_key=True
    )
    task: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(Text)
    file_path : Mapped[str | None] = mapped_column(Text)
    result : Mapped[dict | None] = mapped_column(JSONB(none_as_null=True))
    error : Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    started_at: Mapped[datetime.datetime] = mapped_column(DateTime, Default = None)
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime,Default=None)
    current_attempt : Mapped[int] = mapped_column(Integer, default=0)
    max_attempts : Mapped[int] = mapped_column(Integer, default = 3)

