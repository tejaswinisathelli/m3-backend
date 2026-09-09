from enum import Enum

from typing import Any

from pydantic import BaseModel


class InspectionStatus(str, Enum):

    CREATED = "CREATED"

    PROCESSING = "PROCESSING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


class ComplianceStatus(str, Enum):

    PASS = "PASS"

    FAIL = "FAIL"

    REVIEW = "REVIEW"


class InspectionRequest(BaseModel):

    product: str

    mrp: float

    quantity: str


class QualityResult(BaseModel):

    status: str

    score: float


class TextBlock(BaseModel):

    id: str

    text: str

    confidence: float

    bbox: list[int]


class Declaration(BaseModel):

    value: float

    currency: str | None = None

    confidence: float

    source_regions: list[str]


class M1Result(BaseModel):

    image_id: str

    quality: QualityResult

    text_blocks: list[TextBlock]

    declarations: dict[str, Declaration]

    measurements: list


class M2Result(BaseModel):

    rule_id: str

    field: str

    status: ComplianceStatus

    reason: str

    confidence: float

    evidence_regions: list[str]

    legal_reference: str


class InspectionResponse(BaseModel):

    inspection_id: str

    status: InspectionStatus

    data: InspectionRequest


class InspectionResultResponse(BaseModel):

    inspection_id: str

    status: InspectionStatus

    data: InspectionRequest

    filename: str | None = None

    m1_result: M1Result | None = None

    m2_result: M2Result | None = None


class ImageUploadResponse(BaseModel):

    inspection_id: str

    filename: str

    message: str

    m1_result: M1Result

    m2_result: M2Result


class DashboardResponse(BaseModel):

    total_inspections: int

    passed: int

    failed: int

    review: int


class ReportEvidence(BaseModel):

    region_id: str

    description: str

    bbox: list[int] | None = None


class ReportResponse(BaseModel):

    inspection_id: str

    status: InspectionStatus

    filename: str | None = None

    declarations: dict[str, Any] = {}

    compliance_result: M2Result | None = None

    evidence: list[ReportEvidence] = []

    report_file: str | None = None


class ErrorResponse(BaseModel):

    detail: str