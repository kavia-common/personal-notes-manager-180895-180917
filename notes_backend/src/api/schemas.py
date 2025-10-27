from typing import Optional
from pydantic import BaseModel, Field, constr


class NoteBase(BaseModel):
    title: constr(min_length=1, strip_whitespace=True) = Field(..., description="Title of the note")
    content: constr(min_length=1, strip_whitespace=True) = Field(..., description="Body content of the note")


# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Payload schema for creating a note."""


# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Payload schema for updating a note (partial)."""
    title: Optional[constr(min_length=1, strip_whitespace=True)] = Field(
        default=None, description="Updated title of the note"
    )
    content: Optional[constr(min_length=1, strip_whitespace=True)] = Field(
        default=None, description="Updated content of the note"
    )


# PUBLIC_INTERFACE
class NoteOut(BaseModel):
    """Response schema for returning note details."""
    id: int = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Body content of the note")
    owner_id: str = Field(..., description="Owner/user identifier for the note")
    created_at: float = Field(..., description="Creation timestamp (epoch seconds)")
    updated_at: float = Field(..., description="Last update timestamp (epoch seconds)")
