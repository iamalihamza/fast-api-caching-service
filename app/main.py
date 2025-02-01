from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

from .database import init_db, get_session
from .schemas import (
    PayloadCreateRequest,
    PayloadCreateResponse,
    PayloadReadResponse
)
from .crud import (
    get_transformed_string,
    get_or_create_payload,
    get_payload_by_id
)

app = FastAPI(title="Caching Service")


@app.on_event("startup")
def on_startup():
    # Initialize the database (create tables if not exist)
    init_db()


@app.post("/payload", response_model=PayloadCreateResponse)
def create_payload(data: PayloadCreateRequest, session: Session = Depends(get_session)):
    """
    Create a new payload by:
      - Transforming each string in both lists (caching results).
      - Interleaving them.
      - Storing (or reusing) the final string in 'Payload'.
      - Returning the payload ID and a message.
    """
    list_1 = data.list_1
    list_2 = data.list_2

    if len(list_1) != len(list_2):
        raise HTTPException(status_code=400, detail="Lists must have the same length")

    # Transform and build the final string
    transformed_list_1 = [get_transformed_string(session, s) for s in list_1]
    transformed_list_2 = [get_transformed_string(session, s) for s in list_2]

    # Interleave the two transformed lists
    interleaved = []
    for t1, t2 in zip(transformed_list_1, transformed_list_2):
        interleaved.append(t1)
        interleaved.append(t2)

    final_string = ", ".join(interleaved)

    # Get or create the Payload object
    payload_obj = get_or_create_payload(session, final_string)

    return PayloadCreateResponse(
        payload_id=payload_obj.id,
        message="Payload created or re-used successfully"
    )


@app.get("/payload/{payload_id}", response_model=PayloadReadResponse)
def read_payload(payload_id: int, session: Session = Depends(get_session)):
    """
    Retrieve an existing payload by ID. Returns 404 if not found.
    """
    payload_obj = get_payload_by_id(session, payload_id)
    if not payload_obj:
        raise HTTPException(status_code=404, detail="Payload not found")

    return PayloadReadResponse(output=payload_obj.final_string)
