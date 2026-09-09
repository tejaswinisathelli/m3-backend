from fastapi import APIRouter, UploadFile, File, HTTPException, Header
import uuid

from services.inspection_service import process_image

from schemas.inspection import (
    InspectionRequest,
    InspectionResponse,
    InspectionResultResponse,
    ImageUploadResponse,
    DashboardResponse,
    ReportResponse,
    ReportEvidence,
    ErrorResponse
)

from auth.schemas import (
    LoginRequest,
    LoginResponse
)

from auth.security import (
    authenticate_user,
    create_access_token,
    require_authentication
)

from integrations.m4_mock import (
    save_with_m4,
    get_with_m4,
    get_all_with_m4,
    get_dashboard_with_m4
)


router = APIRouter(
    prefix="/api",
    tags=["Inspections"]
)


@router.post(
    "/inspections",
    response_model=InspectionResponse
)
def create_inspection(data: InspectionRequest):
    inspection_id = str(uuid.uuid4())

    inspection_data = {
        "inspection_id": inspection_id,
        "status": "CREATED",
        "data": data.model_dump()
    }

    save_with_m4(
        inspection_id,
        inspection_data
    )

    return {
        "inspection_id": inspection_id,
        "status": "CREATED",
        "data": data
    }


@router.post(
    "/inspections/{inspection_id}/images",
    response_model=ImageUploadResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def upload_image(
    inspection_id: str,
    image: UploadFile = File(...)
):
    if get_with_m4(inspection_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    allowed_extensions = {".jpg", ".jpeg", ".png"}

    if not image.filename:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format"
        )

    if not image.filename.lower().endswith(
        tuple(allowed_extensions)
    ):
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format"
        )

    try:
        pipeline_result = process_image(
            image.filename,
            inspection_id
        )
    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Pipeline processing failed"
        )

    return {
        "inspection_id": inspection_id,
        "filename": image.filename,
        "message": "Image received",
        "m1_result": pipeline_result["m1_result"],
        "m2_result": pipeline_result["m2_result"]
    }


@router.get(
    "/inspections/{inspection_id}",
    response_model=InspectionResultResponse,
    responses={
        404: {"model": ErrorResponse}
    }
)
def get_inspection_result(inspection_id: str):
    result = get_with_m4(inspection_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    return result


@router.get(
    "/inspections",
    response_model=list[InspectionResultResponse]
)
def get_all_inspection_results():
    return get_all_with_m4()


@router.get(
    "/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    authorization: str = Header(...)
):
    require_authentication(authorization)
    return get_dashboard_with_m4()


@router.get(
    "/reports/{inspection_id}",
    response_model=ReportResponse,
    responses={
        404: {"model": ErrorResponse}
    }
)
def get_report(inspection_id: str):
    inspection = get_with_m4(inspection_id)

    if inspection is None:
        raise HTTPException(
            status_code=404,
            detail="Inspection not found"
        )

    m1_result = inspection.get("m1_result")
    m2_result = inspection.get("m2_result")

    declarations = {}

    if m1_result:
        declarations = m1_result.get(
            "declarations",
            {}
        )

    evidence = []

    if m1_result:
        text_blocks = m1_result.get(
            "text_blocks",
            []
        )

        for block in text_blocks:
            evidence.append(
                ReportEvidence(
                    region_id=block["id"],
                    description=block["text"],
                    bbox=block.get("bbox")
                )
            )

    return {
        "inspection_id": inspection_id,
        "status": inspection.get(
            "status",
            "CREATED"
        ),
        "filename": inspection.get("filename"),
        "declarations": declarations,
        "compliance_result": m2_result,
        "evidence": evidence,
        "report_file": None
    }


@router.post(
    "/auth/login",
    response_model=LoginResponse
)
def login(data: LoginRequest):
    role = authenticate_user(
        data.username,
        data.password
    )

    if role is not None:
        access_token = create_access_token(
            data.username,
            role
        )

        return {
            "message": "Login successful",
            "username": data.username,
            "role": role,
            "authenticated": True,
            "access_token": access_token
        }

    return {
        "message": "Invalid username or password",
        "username": data.username,
        "role": None,
        "authenticated": False,
        "access_token": None
    }