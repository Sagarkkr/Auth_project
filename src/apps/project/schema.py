from datetime import timezone
from pydantic import BaseModel, Field
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Project(BaseModel):
    name: str | None = StringField(required=True, unique=True)
    description: str | None = StringField()
    created_at:datetime | None = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(Project, self).save(*args, **kwargs)
