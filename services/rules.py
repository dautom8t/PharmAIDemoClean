"""
Rules engine.

Stores rules in the database and evaluates them against workflows.
Rules are simple: each rule has a `condition` string and an `action` string.

NOTE (demo): This evaluates Python expressions. Do NOT run untrusted rule
content in production without sandboxing.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.schemas import RuleCreate
from models import database
from models.rules import Rule  # <-- If you DO NOT have models/rules.py, tell me and I’ll adjust.


def create_rule(db: Session, rule_in: RuleCreate) -> Rule:
    rule = Rule(
        name=rule_in.name,
        description=rule_in.description,
        condition=rule_in.condition,
        action=rule_in.action,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


def list_rules(db: Session):
    return db.query(Rule).all()


def evaluate_rules_for_workflow(db: Session, workflow) -> None:
    """
    Evaluate all rules against a given workflow.

    This mutates the workflow/tasks in-memory. The caller is responsible for committing.
    """
    rules = list_rules(db)
    if not rules:
        return

    # Provide a minimal safe-ish evaluation context
    ctx = {
        "workflow": workflow,
        "TaskState": __import__("models.schemas", fromlist=["TaskState"]).TaskState,
        "WorkflowState": __import__("models.schemas", fromlist=["WorkflowState"]).WorkflowState,
    }

    for rule in rules:
        try:
            if bool(eval(rule.condition, {"__builtins__": {}}, ctx)):
                exec(rule.action, {"__builtins__": {}}, ctx)
        except Exception:
            # Demo: ignore bad rules rather than crashing the API
            continue
