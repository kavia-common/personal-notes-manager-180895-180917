from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ..dependencies import require_auth
from ..models import repository, Note
from ..schemas import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


def _to_note_out(note: Note) -> NoteOut:
    return NoteOut(
        id=note.id,
        title=note.title,
        content=note.content,
        owner_id=note.owner_id,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note for the current user.",
    responses={
        201: {"description": "Note created"},
        400: {"description": "Validation error"},
        401: {"description": "Unauthorized"},
    },
)
def create_note(payload: NoteCreate, user_id: str = Depends(require_auth)) -> NoteOut:
    """
    Create a new note.

    Parameters:
        payload: NoteCreate body with title and content.
        user_id: Injected current user id.

    Returns:
        NoteOut: The created note.
    """
    note = repository.create(title=payload.title, content=payload.content, owner_id=user_id)
    return _to_note_out(note)


@router.get(
    "",
    response_model=List[NoteOut],
    status_code=status.HTTP_200_OK,
    summary="List notes",
    description="List all notes for the current user (placeholder behavior; no strict isolation enforced).",
    responses={
        200: {"description": "List of notes"},
        401: {"description": "Unauthorized"},
    },
)
def list_notes(user_id: str = Depends(require_auth)) -> List[NoteOut]:
    """
    List notes for the current user.

    Parameters:
        user_id: Injected current user id.

    Returns:
        List[NoteOut]: A list of notes.
    """
    notes = repository.list_all(owner_id=user_id)
    return [_to_note_out(n) for n in notes]


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    status_code=status.HTTP_200_OK,
    summary="Get note",
    description="Retrieve a note by id.",
    responses={
        200: {"description": "Note found"},
        404: {"description": "Note not found"},
        401: {"description": "Unauthorized"},
    },
)
def get_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    user_id: str = Depends(require_auth),
) -> NoteOut:
    """
    Get a specific note.

    Parameters:
        note_id: Path parameter identifying the note.
        user_id: Injected current user id.

    Returns:
        NoteOut: The requested note.

    Raises:
        HTTPException(404): If not found.
    """
    note = repository.get(note_id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    # Optional: enforce owner check in future
    return _to_note_out(note)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    status_code=status.HTTP_200_OK,
    summary="Update note",
    description="Update a note's title/content.",
    responses={
        200: {"description": "Note updated"},
        400: {"description": "Validation error"},
        404: {"description": "Note not found"},
        401: {"description": "Unauthorized"},
    },
)
def update_note(
    payload: NoteUpdate,
    note_id: int = Path(..., ge=1, description="ID of the note"),
    user_id: str = Depends(require_auth),
) -> NoteOut:
    """
    Update a specific note.

    Parameters:
        payload: NoteUpdate with optional title/content.
        note_id: Path parameter ID.
        user_id: Injected current user id.

    Returns:
        NoteOut of updated note.

    Raises:
        HTTPException(404): If note not found.
        HTTPException(400): If payload contains neither title nor content.
    """
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    note = repository.update(note_id, title=payload.title, content=payload.content)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return _to_note_out(note)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by id.",
    responses={
        204: {"description": "Note deleted"},
        404: {"description": "Note not found"},
        401: {"description": "Unauthorized"},
    },
)
def delete_note(
    note_id: int = Path(..., ge=1, description="ID of the note"),
    user_id: str = Depends(require_auth),
) -> None:
    """
    Delete a specific note.

    Parameters:
        note_id: Path parameter ID.
        user_id: Injected current user id.

    Returns:
        None (204 No Content)

    Raises:
        HTTPException(404): If note not found.
    """
    deleted = repository.delete(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
