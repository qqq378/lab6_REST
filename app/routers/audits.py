from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models import Audit, AuditCreate
from app.store import audit_store

router = APIRouter(prefix="/api/v1/audits", tags=["audits"])


@router.get("/", response_model=List[Audit], status_code=status.HTTP_200_OK,
            summary="Получить список аудитов")
def list_audits():
    return audit_store.list()


@router.get("/{audit_id}", response_model=Audit, status_code=status.HTTP_200_OK,
            summary="Получить аудит по идентификатору",
            responses={404: {"description": "Аудит не найден"}})
def get_audit(audit_id: int):
    record = audit_store.get(audit_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Аудит с id={audit_id} не найден")
    return record


@router.post("/", response_model=Audit, status_code=status.HTTP_201_CREATED,
             summary="Создать новый аудит",
             responses={400: {"description": "Некорректные входные данные"}})
def create_audit(payload: AuditCreate):
    return audit_store.create(payload)


@router.delete("/{audit_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить аудит",
               responses={404: {"description": "Аудит не найден"}})
def delete_audit(audit_id: int):
    if not audit_store.delete(audit_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Аудит с id={audit_id} не найден")
