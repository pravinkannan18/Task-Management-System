from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_project(db, project, current_user.id)

@router.get("/", response_model=list[schemas.Project])
def list_projects(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_projects(db, current_user.id)

@router.get("/{id}", response_model=schemas.Project)
def get_project(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    project = crud.get_project(db, id, current_user.id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.patch("/{id}", response_model=schemas.Project)
def update_project(id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    updated_project = crud.update_project(db, id, project, current_user.id)
    if not updated_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return updated_project

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    project = crud.delete_project(db, id, current_user.id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")