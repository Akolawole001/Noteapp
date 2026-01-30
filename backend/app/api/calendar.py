"""
Calendar Events API endpoints.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user
from app.domain.models import User, CalendarEvent, Task
from app.domain.schemas import CalendarEventCreate, CalendarEventUpdate, CalendarEventResponse


router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/", response_model=List[CalendarEventResponse])
def get_events(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get calendar events for current user.
    
    - Optional filtering by date range
    - Supports pagination
    - Returns only user's own events
    """
    query = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id)
    
    # Apply date range filters if provided
    if start_date:
        query = query.filter(CalendarEvent.start_time >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.end_time <= end_date)
    
    # Apply pagination and ordering
    events = query.order_by(CalendarEvent.start_time.asc()).offset(skip).limit(limit).all()
    
    return events


@router.get("/{event_id}", response_model=CalendarEventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific calendar event by ID with ownership validation."""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar event not found"
        )
    
    return event


@router.post("/", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: CalendarEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new calendar event.
    
    - Validates time range
    - Optional task linking (validates task ownership)
    - Checks for conflicts (optional)
    """
    # Validate linked task if provided
    if event_data.linked_task_id:
        linked_task = db.query(Task).filter(
            Task.id == event_data.linked_task_id,
            Task.user_id == current_user.id
        ).first()
        
        if not linked_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Linked task not found or not owned by user"
            )
    
    # Check for time conflicts (optional - can be made stricter)
    conflict = db.query(CalendarEvent).filter(
        CalendarEvent.user_id == current_user.id,
        CalendarEvent.start_time < event_data.end_time,
        CalendarEvent.end_time > event_data.start_time
    ).first()
    
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event conflicts with existing event: {conflict.title}"
        )
    
    # Create event
    db_event = CalendarEvent(
        user_id=current_user.id,
        title=event_data.title,
        description=event_data.description,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        linked_task_id=event_data.linked_task_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event


@router.put("/{event_id}", response_model=CalendarEventResponse)
def update_event(
    event_id: int,
    event_data: CalendarEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update an existing calendar event with ownership validation."""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar event not found"
        )
    
    # Validate linked task if being updated
    if event_data.linked_task_id is not None:
        if event_data.linked_task_id != 0:  # 0 means remove link
            linked_task = db.query(Task).filter(
                Task.id == event_data.linked_task_id,
                Task.user_id == current_user.id
            ).first()
            
            if not linked_task:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Linked task not found or not owned by user"
                )
    
    # Update fields if provided
    if event_data.title is not None:
        event.title = event_data.title
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.start_time is not None:
        event.start_time = event_data.start_time
    if event_data.end_time is not None:
        event.end_time = event_data.end_time
    if event_data.linked_task_id is not None:
        event.linked_task_id = event_data.linked_task_id if event_data.linked_task_id != 0 else None
    
    # Validate time range if updated
    if event.end_time <= event.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_time must be after start_time"
        )
    
    db.commit()
    db.refresh(event)
    
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a calendar event with ownership validation."""
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == current_user.id
    ).first()
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calendar event not found"
        )
    
    db.delete(event)
    db.commit()
    
    return None
