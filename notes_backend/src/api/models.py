from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Note:
    """
    Domain model for a Note (storage layer representation).
    This is separate from API schemas to decouple persistence from I/O contracts.
    """
    id: int
    title: str
    content: str
    owner_id: str
    created_at: float = field(default_factory=lambda: time.time())
    updated_at: float = field(default_factory=lambda: time.time())


class InMemoryNoteRepository:
    """
    A simple thread-safe in-memory repository for Notes.
    Predictable, auto-incrementing IDs and per-process lifetime.

    TODO:
        - Replace with real database (e.g., Postgres/SQLite) implementation.
        - Add indexing and query support for filtering by owner_id if multi-user isolation is required.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._notes: Dict[int, Note] = {}
        self._next_id = 1

    def _generate_id(self) -> int:
        with self._lock:
            nid = self._next_id
            self._next_id += 1
            return nid

    # PUBLIC_INTERFACE
    def create(self, title: str, content: str, owner_id: str) -> Note:
        """Create and persist a new note."""
        with self._lock:
            nid = self._generate_id()
            now = time.time()
            note = Note(id=nid, title=title, content=content, owner_id=owner_id, created_at=now, updated_at=now)
            self._notes[nid] = note
            return note

    # PUBLIC_INTERFACE
    def list_all(self, owner_id: Optional[str] = None) -> List[Note]:
        """List all notes, optionally filtering by owner_id."""
        with self._lock:
            items = list(self._notes.values())
            if owner_id is not None:
                items = [n for n in items if n.owner_id == owner_id]
            # return a copy to avoid external mutation
            return list(items)

    # PUBLIC_INTERFACE
    def get(self, note_id: int) -> Optional[Note]:
        """Retrieve a single note by id."""
        with self._lock:
            return self._notes.get(note_id)

    # PUBLIC_INTERFACE
    def update(self, note_id: int, *, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Note]:
        """Update a note's title and/or content."""
        with self._lock:
            note = self._notes.get(note_id)
            if note is None:
                return None
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            note.updated_at = time.time()
            return note

    # PUBLIC_INTERFACE
    def delete(self, note_id: int) -> bool:
        """Delete a note by id. Returns True if deleted, False if not found."""
        with self._lock:
            return self._notes.pop(note_id, None) is not None


# Singleton repository instance for app lifetime.
repository = InMemoryNoteRepository()
