from fastapi import HTTPException

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository

class NoteService:
    def __init__(
        self, 
        noteRepository: NoteRepository,
        labelRepository: LabelRepository,
        shareRepository: ShareRepository
    ):
        self.noteRepository = noteRepository
        self.labelRepository = labelRepository
        self.shareRepository = shareRepository

    def user_can_read(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shareRepository.has_note_share(note_id=note.id, user_id=user_id):
            return True

        label_ids = self.labelRepository.list_label_ids_for_note(note.id)
        return self.shareRepository.has_any_label_share(label_ids=label_ids, user_id=user_id)

    def user_can_edit(self, user_id: int, note: Note) -> bool:
        if note.owner_id == user_id:
            return True

        if self.shareRepository.is_note_share(note_id=note.id, user_id=user_id, role=ShareRole.EDIT):
            return True

        label_ids = self.labelRepository.list_labels_ids_for_note(note.id)
        return self.shareRepository.has_any_label_share(label_ids=label_ids, user_id=user_id, role=ShareRole.EDIT)

    def list_visible(self, user_id: int) -> list[Note]:
        owned = self.noteRepository.list_owned(user_id)

        direct_ids = self.shareRepository.list_note_ids_shared_with_user(user_id)

        shared_label_ids = self.shareRepository.list_label_ids_shared_with_user(user_id)
        ids_by_label = self.labelRepository.list_note_ids_by_label_ids(shared_label_ids)

        combined_ids = list({*direct_ids, *ids_by_label})
        shared = self.noteRepository.list_by_ids(combined_ids)

        combined = {note.id: note for note in owned}

        for note in shared:
            combined.setdefault(note.id, note)

        return sorted(combined.values(), key=lambda note: note.id, reverse=True)
    
    def create(self, owner_id: int, payload: NoteCreate) -> Note:
        note = self.noteRepository.create(
            Note(owner_id=owner_id, **
                 payload.model_dump(exclude={"label_ids"}))
        )

        if payload.label_ids:
            self._set_labels(owner_id, note.id, payload.label_ids)

        return note

    def update(self, user_id: int, note_id: int, payload: NoteUpdate) -> Note:
        note = self.noteRepository.get_by_id(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        if not self.user_can_edit(user_id, note):
            raise HTTPException(status_code=403, detail="Unauthorized")

        updates = payload.model_dump(exclude_none=True)
        label_ids = updates.pop("label_ids", None)

        for key, value in updates.items():
            setattr(note, key, value)

        note = self.noteRepository.update(note)

        if label_ids is not None:
            if note.owner_id != user_id:
                raise HTTPException(
                    status_code=404, detail="Doesn't exist or not authorized")
            self._set_labels(user_id, note.id, label_ids)

        return note

    def delete(self, user_id: int, note_id: int) -> None:
        note = self.noteRepository.get_by_id(note_id)
        if not note or note.owner_id != user_id:
            raise HTTPException(
                status_code=404, detail="Note doesn't exist or unauthorized")
        self.noteRepository.delete(note)

    def _set_labels(self, owner_id: int, note_id: int, label_ids: list[int]) -> None:
        valid_ids = self.labelRepository.list_ids_for_owner_subset(
            owner_id, label_ids or [])
        self.noteRepository.replace_labels(owner_id, note_id, valid_ids)