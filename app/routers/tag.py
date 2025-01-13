from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.tag import Tag, TagCreate
from app.services.tag_service import TagService
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Tag)
async def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    created_tag = tag_service.create_tag(tag)
    return created_tag

@router.get("/{tag_id}", response_model=Tag)
async def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    tag = tag_service.get_tag(tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/", response_model=List[Tag])
async def get_all_tags(db: Session = Depends(get_db)):
    tag_service = TagService(db)
    return tag_service.get_all_tags()

@router.put("/{tag_id}", response_model=Tag)
async def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    updated_tag = tag_service.update_tag(tag_id, tag)
    if updated_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag

@router.delete("/{tag_id}", response_model=bool)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    success = tag_service.delete_tag(tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return success