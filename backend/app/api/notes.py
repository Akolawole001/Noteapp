"""
Notes API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.domain.models import User, Note
from app.domain.schemas import NoteCreate, NoteUpdate, NoteResponse


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=List[NoteResponse])
def get_notes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all notes for current user with pagination and search.
    
    - Supports pagination (skip, limit)
    - Optional search by title
    - Returns only user's own notes
    """
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    # Apply search filter if provided
    if search:
        query = query.filter(Note.title.ilike(f"%{search}%"))
    
    # Apply pagination and ordering
    notes = query.order_by(Note.updated_at.desc()).offset(skip).limit(limit).all()
    
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific note by ID.
    
    - Validates ownership
    - Returns 404 if not found or not owned by user
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return note


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new note.
    
    - Associates note with current user
    - Returns created note
    """
    db_note = Note(
        user_id=current_user.id,
        title=note_data.title,
        content=note_data.content
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing note.
    
    - Validates ownership
    - Only updates provided fields
    - Returns updated note
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    # Update fields if provided
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a note.
    
    - Validates ownership
    - Permanently removes note
    """
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(note)
    db.commit()
    
    return None
