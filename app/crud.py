from typing import Optional
from sqlmodel import select, Session
from .models import CachedTransform, Payload


def get_transformed_string(session: Session, original_string: str) -> str:
    """
    Check if 'original_string' is in the cache (CachedTransform).
    If found, return the cached transformed_string.
    If not, transform (simulate external call), save, then return it.
    """
    statement = select(CachedTransform).where(CachedTransform.original_string == original_string)
    result = session.exec(statement).first()

    if result:
        return result.transformed_string

    # Simulate "transformer function" by converting to uppercase
    transformed_string = original_string.upper()

    # Save in cache
    new_record = CachedTransform(
        original_string=original_string,
        transformed_string=transformed_string
    )
    session.add(new_record)
    session.commit()
    session.refresh(new_record)

    return transformed_string


def get_or_create_payload(session: Session, final_string: str) -> Payload:
    """
    If 'final_string' already exists in Payload, return it.
    Otherwise create a new one.
    """
    statement = select(Payload).where(Payload.final_string == final_string)
    existing = session.exec(statement).first()

    if existing:
        return existing

    new_payload = Payload(final_string=final_string)
    session.add(new_payload)
    session.commit()
    session.refresh(new_payload)
    return new_payload


def get_payload_by_id(session: Session, payload_id: int) -> Optional[Payload]:
    """
    Retrieve a Payload record by ID, or None if it doesn't exist.
    """
    return session.get(Payload, payload_id)
