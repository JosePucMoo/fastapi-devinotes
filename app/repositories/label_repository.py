
from sqlmodel import Session, select, delete

from app.models.label import Label, NoteLabelLink
from app.models.share import LabelShare


class LabelRepository:
    def __init__(self, db:Session):
        self.db = db
    
    def get_by_id(self, label_id: int) -> Label | None:
        return self.db.get(Label, label_id)
    
    def get_by_name(self, owner_id: int, name: str) -> Label | None:
        query = select(Label).where(
            Label.owner_id == owner_id, 
            Label.name == name
        )
        return self.db.exec(query).first()
    
    def list_by_user(self, owner_id: int) -> list[Label]:
        query = select(Label).where(Label.owner_id == owner_id).order_by(Label.id.asc())
        
        return self.db.exec(query).all()
    
    def create(self, owner_id: int, name: str) -> Label:
        label = Label(owner_id=owner_id, name=name)
        
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label
    
    def update(self, label: Label) -> Label:
        self.db.add(label)
        self.db.commit()
        self.db.refresh(label)
        return label
    
    def delete(self, label: Label) -> None:
        self.db.exec(
            delete(NoteLabelLink).where(
                NoteLabelLink.label_id == label.id
            )
        )
        
        self.db.exec(
            delete(LabelShare).where(
                LabelShare.label_id == label.id
            )
        )
        
        self.db.delete(label)
        self.db.commit()
        
    def list_ids_for_owner_subset(self, owner_id: int, label_ids: list[int]) -> list[int]:
        if not label_ids:
            return []
        
        return self.db.exec(
            select(Label.id).where(
                Label.owner_id == owner_id,
                Label.id.in_(set(label_ids))
            )
        ).all()
        
    def list_labels_ids_for_note(self, note_id: int) -> list[int]:        
        return self.db.exec(
            select(NoteLabelLink.label_id).where(
                NoteLabelLink.note_id == note_id
            )
        ).all()
        
    def list_note_ids_by_label_ids(self, label_ids: list[int]) -> list[int]:        
        if not label_ids:
            return []
        
        return self.db.exec(
            select(NoteLabelLink.note_id).where(
                NoteLabelLink.label_id.in_(label_ids)
            )
        ).all()