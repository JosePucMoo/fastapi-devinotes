from fastapi import HTTPException
from sqlmodel import Session

from app.models.label import Label, LabelCreate
from app.repositories.label_repository import LabelRepository


class LabelService:

    def __init__(self, labelRepository: LabelRepository):
        self.labelRepository = labelRepository

    def list(self, owner_id: int) -> list[Label]:
        return self.labelRepository.list_by_user(owner_id)

    def create(self, owner_id: int, payload: LabelCreate) -> Label:
        if self.labelRepository.get_by_name(owner_id, payload.name):
            raise HTTPException(
                status_code=400, detail="Label already exist")

        return self.labelRepository.create(owner_id, payload.name)

    def delete(self, owner_id: int, label_id: int) -> None:
        label = self.labelRepository.get_by_id(label_id)
        if not label or label.owner_id != owner_id:
            raise HTTPException(
                status_code=404, detail="Label doesn't exist or unauthorized")

        self.labelRepository.delete(label)