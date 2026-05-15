from fastapi import HTTPException
from sqlmodel import Session

from app.models.share import ShareRole
from app.repositories.label_repository import LabelRepository
from app.repositories.note_repository import NoteRepository
from app.repositories.share_repository import ShareRepository


class ShareService:
    def __init__(
        self, 
        shareRepository: ShareRepository,
        noteRepository: NoteRepository,
        labelRepository: LabelRepository
    ):
        self.shareRepository = shareRepository
        self.noteRepository = noteRepository
        self.labelRepository = labelRepository

    def share_note(self, owner_id: int, note_id: int, target_user_id: int, role: ShareRole):
        note = self.noteRepository.get_by_id(note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Note doesn't exist or unauthorized")

        share = self.shareRepository.upsert_note_share(
            note_id, target_user_id, role.value if hasattr(role, "value") else role)

        return share

    def unshare_note(self, owner_id: int, note_id: int, target_user_id: int):
        note = self.noteRepository.get_by_id(note_id)

        if not note or note.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Note doesn't exist or unauthorized")

        self.shareRepository.remove_note_share(note_id, target_user_id)

    def share_label(self, owner_id: int, label_id: int, target_user_id: int, role: ShareRole):
        label = self.labelRepository.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Label doesn't exist or unauthorized")

        share = self.shareRepository.upsert_label_share(
            label_id, target_user_id, role.value)

        return share

    def unshare_label(self, owner_id: int, label_id: int, target_user_id: int):
        label = self.labelRepository.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Label doesn't exist or unauthorized")

        self.shareRepository.remove_label_share(label_id, target_user_id)