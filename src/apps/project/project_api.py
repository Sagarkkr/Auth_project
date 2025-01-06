from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.apps.authentication.roles import admin_required, get_current_user
from src.apps.project import project_dao
from src.apps.project.schema import Project

router = APIRouter()

@router.post("/project")
async def create_project(body:Project,current_user=Depends(admin_required)):
    project = await project_dao.fetch_project_details_dao({"name": body.model_dump().get('name')})
    if project:
        return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content="Project with this name already exists"
            )    
    await project_dao.create_project_dao(body.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content="Project created successfully")


@router.get("/project")
async def get_projects(current_user=Depends(get_current_user)):
    projects = Project.objects.all()
    return {"projects": [project.to_mongo() for project in projects]}

@router.put("/project/{project_id}")
async def update_project(project_id: str, name: str = None, description: str = None, current_user=Depends(admin_required)):
    project = Project.objects(id=project_id).first()
    if not project:
        raise JSONResponse(status_code=404, content="Project not found")
    
    if name:
        project.name = name
    if description:
        project.description = description
    project.save()
    return {"message": "Project updated successfully", "project": project.to_mongo()}
