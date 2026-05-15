from fastapi import APIRouter, status

from app.api.dependencies import CurrentUser, DBSession
from app.models.note import NoteCreate, NoteRead, NoteUpdate
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository
from app.services.note_service import NoteService


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(db: DBSession, user: CurrentUser):
    noteRepository = NoteRepository(db)
    labelRepository = LabelRepository(db)
    shareRepository = ShareRepository(db)
    
    noteService = NoteService(
        noteRepository=noteRepository,
        labelRepository=labelRepository,
        shareRepository=shareRepository
    )
    return noteService.list_visible(user.id)


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: DBSession, user: CurrentUser):
    noteRepository = NoteRepository(db)
    labelRepository = LabelRepository(db)
    shareRepository = ShareRepository(db)
    
    noteService = NoteService(
        noteRepository=noteRepository,
        labelRepository=labelRepository,
        shareRepository=shareRepository
    )
    return noteService.create(user.id, payload)


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: DBSession, user: CurrentUser):
    noteRepository = NoteRepository(db)
    labelRepository = LabelRepository(db)
    shareRepository = ShareRepository(db)
    
    noteService = NoteService(
        noteRepository=noteRepository,
        labelRepository=labelRepository,
        shareRepository=shareRepository
    )
    return noteService.update(user.id, note_id, payload)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: DBSession, user: CurrentUser):
    noteRepository = NoteRepository(db)
    labelRepository = LabelRepository(db)
    shareRepository = ShareRepository(db)
    
    noteService = NoteService(
        noteRepository=noteRepository,
        labelRepository=labelRepository,
        shareRepository=shareRepository
    )
    noteService.delete(user.id, note_id)

    return None