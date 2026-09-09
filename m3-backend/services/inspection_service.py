import logging

from integrations.m1_mock import mock_m1
from integrations.m2_mock import process_with_m2
from integrations.m4_mock import save_with_m4


logger = logging.getLogger(__name__)


def process_image(image_filename: str, inspection_id: str):
    logger.info(
        "Starting inspection processing: %s",
        inspection_id
    )

    # Step 1: Mark inspection as PROCESSING
    save_with_m4(
        inspection_id,
        {
            "status": "PROCESSING"
        }
    )

    try:
        # Step 2: Send image information to M1
        m1_result = mock_m1(
            image_id=image_filename
        )

        # Step 3: Send M1 result to M2
        m2_result = process_with_m2(
            m1_result
        )

    except Exception as e:
        logger.error(
            "Inspection processing failed: %s",
            inspection_id,
            exc_info=True
        )

        # Step 4: Mark inspection as FAILED if pipeline fails
        save_with_m4(
            inspection_id,
            {
                "status": "FAILED"
            }
        )

        raise RuntimeError(
            "Pipeline processing failed"
        ) from e

    # Step 5: Mark processing as COMPLETED
    pipeline_result = {
        "inspection_id": inspection_id,
        "status": "COMPLETED",
        "filename": image_filename,
        "m1_result": m1_result,
        "m2_result": m2_result
    }

    # Step 6: Save completed result through M4
    save_with_m4(
        inspection_id,
        pipeline_result
    )

    logger.info(
        "Inspection processing completed: %s",
        inspection_id
    )

    # Step 7: Return the completed pipeline result
    return pipeline_result