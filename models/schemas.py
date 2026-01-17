"""
Pydantic models and enums used throughout the PharmAI middleware API.

These models define the shape of request and response bodies and enforce
data validation at the API boundary.  Using Pydantic helps catch invalid
inputs early and documents the API automatically.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowState(str, Enum):
    """High level state of a medication workflow."""
    ORDERED = "ordered"            # Initial state after order entry
    PENDING_ACCESS = "pending_access"  # Awaiting benefits verification / prior auth
    ACCESS_GRANTED = "access_granted"  # Coverage approved; ready for dispense
    DISPENSED = "dispensed"            # Medication dispensed to patient
    COMPLETED = "completed"            # Therapy start confirmed
    FAILED = "failed"                  # Workflow terminated due to denial or cancellation


class TaskState(str, Enum):
    """State of an individual workflow task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskBase(BaseModel):
    name: str = Field(..., description="Human‑readable name of the task")
    assigned_to: Optional[str] = Field(
        None, description="Identifier of the person or system responsible for the task"
    )


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskRead(TaskBase):
    """Model returned when reading tasks from the API."""

    id: int
    workflow_id: int
    state: TaskState
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    event_type: str = Field(..., description="Type or name of the event")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary event payload")


class EventCreate(EventBase):
    """Model for creating a new event."""
    pass


class EventRead(EventBase):
    """Model returned when reading events from the API."""
    id: int
    workflow_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class WorkflowBase(BaseModel):
    name: str = Field(..., description="Name or identifier of the workflow")
    description: Optional[str] = Field(None, description="Optional description of the workflow")


class WorkflowCreate(WorkflowBase):
    """Request model for creating a new workflow."""
    initial_tasks: Optional[List[TaskCreate]] = Field(
        None, description="Optional list of tasks to seed the workflow with upon creation"
    )


class WorkflowRead(WorkflowBase):
    """Response model for reading workflow details."""

    id: int
    state: WorkflowState
    created_at: datetime
    updated_at: datetime
    tasks: List[TaskRead] = Field(default_factory=list)
    events: List[EventRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class RuleBase(BaseModel):
    name: str = Field(..., description="Name of the rule")
    description: Optional[str] = Field(None, description="Human readable description")
    condition: str = Field(
        ...,
        description=(
            "A Python expression that takes a workflow and returns True if the rule applies. "
            "E.g. 'workflow.state == WorkflowState.ORDERED'"
        ),
    )
    action: str = Field(
        ...,
        description=(
            "A Python expression executed when the condition is met. "
            "It should mutate the workflow or its tasks, e.g. "
            "'workflow.state = WorkflowState.PENDING_ACCESS'"
        ),
    )


class RuleCreate(RuleBase):
    """Model for creating a new rule."""
    pass


class RuleRead(RuleBase):
    """Model returned when reading rules from the API."""
    id: int

    class Config:
        orm_mode = True