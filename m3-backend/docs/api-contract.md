# API Contract

## Base URL

/api

## Inspection APIs

### 1. Create Inspection

**Method:** POST

**Endpoint:**
/api/inspections

**Request:**
{
    "product": "Biscuit",
    "mrp": 50,
    "quantity": "200g"
}

**Response:**
{
    "inspection_id": "unique-id",
    "status": "CREATED",
    "data": {
        "product": "Biscuit",
        "mrp": 50,
        "quantity": "200g"
    }
}


### 2. Upload Image

**Method:** POST

**Endpoint:**

/api/inspections/{inspection_id}/images

**Input:**

Image file

**Purpose:**

Accept an image for an existing inspection and pass the image information through the M3 pipeline.

**Current mock response:**

{
    "inspection_id": "unique-id",
    "filename": "image.png",
    "message": "Image received",
    "m1_result": {},
    "m2_result": {}
}

**Error Responses:**

If the inspection does not exist:

**HTTP Status:** 404

{
    "detail": "Inspection not found"
}

If the image format is not supported:

**HTTP Status:** 400

{
    "detail": "Unsupported image format"
}

If pipeline processing fails:

**HTTP Status:** 500

{
    "detail": "Pipeline processing failed"
}

**Notes:**

- M3 owns the upload endpoint and orchestration.

- M1 owns image processing, OCR, and information extraction.

- M2 owns compliance decisions.

- The current M1 and M2 responses are mock responses and may change when the real module contracts are finalized.


### 3. Get Inspection

**Method:** GET

**Endpoint:**
/api/inspections/{inspection_id}

**Purpose:**
Retrieve the stored result of a specific inspection.

**Successful Response:**
{
    "inspection_id": "unique-id",
    "filename": "image.png",
    "m1_result": {},
    "m2_result": {}
}

**Error Response:**
If the inspection does not exist:

**HTTP Status:** 404

{
    "detail": "Inspection not found"
}

**Notes:**
- M3 provides the API endpoint.
- M4 provides the persistence/repository layer.
- The response structure may evolve when the final inspection contract is frozen.

### 4. Get All Inspections

**Method:** GET

**Endpoint:**
/api/inspections

**Purpose:**
Retrieve the stored results of all inspections.

**Successful Response:**
[
    {
        "inspection_id": "unique-id",
        "filename": "image.png",
        "m1_result": {},
        "m2_result": {}
    }
]

**Notes:**
- M3 provides the API endpoint.
- M4 provides the persistence/repository layer.
- The response structure may evolve when the final inspection contract is frozen.


### 5. Get Dashboard

**Method:** GET

**Endpoint:**
/api/dashboard

**Purpose:**
Return summary information about the inspections processed by the backend.

**Successful Response:**
{
    "total_inspections": 1,
    "passed": 0,
    "failed": 0,
    "review": 1
}

**Notes:**
- M3 provides the dashboard API.
- The summary is calculated from inspection results available through the repository layer.
- PASS, FAIL, and REVIEW correspond to compliance results returned by the compliance module.