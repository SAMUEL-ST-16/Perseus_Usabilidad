"""
Requirements Router
Defines API endpoints for requirement extraction and processing
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse
from app.schemas.models import (
    SingleCommentRequest,
    PlayStoreURLRequest,
    ProcessingResponse,
    HealthResponse
)
from app.services.orchestrator import orchestrator_service
from app.services.huggingface_service import huggingface_service
from app.core.logger import get_logger
from app.core.exceptions import (
    PerseusException,
    ValidationException,
    FileProcessingException,
    ScrapingException
)

logger = get_logger(__name__)

router = APIRouter()


# ========== Health Check ==========

@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Check API health status"
)
async def health_check():
    """
    Check the health status of the API and loaded models
    """
    logger.info("Health check requested")

    model_status = huggingface_service.is_loaded()
    model_info = huggingface_service.get_model_info()

    return HealthResponse(
        status="healthy",
        binary_model_loaded=model_status["binary"],
        multiclass_model_loaded=model_status["multiclass"],
        binary_model_name=model_info["binary_model"],
        multiclass_model_name=model_info["multiclass_model"]
    )


# ========== Process Endpoints (Return PDF) ==========

@router.post(
    "/process/single",
    tags=["Requirements Extraction"],
    summary="Process single comment and return PDF",
    response_class=StreamingResponse
)
async def process_single_comment(request: SingleCommentRequest):
    """
    Process a single comment and return PDF report

    Args:
        request: Single comment request

    Returns:
        PDF file with requirement analysis
    """
    try:
        logger.info(f"Processing single comment: {request.comment[:100]}...")

        # Process and get PDF
        response, pdf_buffer = await orchestrator_service.process_single_comment(
            request.comment
        )

        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=requisitos_usabilidad_perseus.pdf"
            }
        )

    except PerseusException as e:
        logger.error(f"Processing error: {e.message}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/process/csv",
    tags=["Requirements Extraction"],
    summary="Process CSV file and return PDF",
    response_class=StreamingResponse
)
async def process_csv_file(file: UploadFile = File(...)):
    """
    Process CSV file with multiple comments and return PDF report

    Args:
        file: Uploaded CSV file

    Returns:
        PDF file with requirement analysis
    """
    try:
        logger.info(f"Processing CSV file: {file.filename}")

        # Validate file extension
        if not file.filename.endswith('.csv'):
            raise ValidationException("File must be a CSV file")

        # Process and get PDF
        response, pdf_buffer = await orchestrator_service.process_csv_file(file)

        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=requisitos_{file.filename.replace('.csv', '.pdf')}"
            }
        )

    except FileProcessingException as e:
        logger.error(f"File processing error: {e.message}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/process/playstore",
    tags=["Requirements Extraction"],
    summary="Process Play Store URL with smart scraping and return PDF",
    response_class=StreamingResponse
)
async def process_playstore_url(request: PlayStoreURLRequest):
    """
    Process Google Play Store URL with intelligent filtering and return PDF report

    Smart scraping filters:
    - Rating: 2-3 stars (critical feedback)
    - Minimum: 15+ words per comment
    - Target: 30 valid requirements
    - Maximum: 500 reviews analyzed

    Args:
        request: Play Store URL request

    Returns:
        PDF file with requirement analysis
    """
    try:
        logger.info(f"Processing Play Store URL with smart scraping: {request.url}")

        # Process with smart scraping (30 requirements, max 500 reviews)
        response, pdf_buffer = await orchestrator_service.process_playstore_url(
            request.url,
            target_requirements=30,
            max_total_reviews=500
        )

        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=requisitos_playstore.pdf"
            }
        )

    except ScrapingException as e:
        logger.error(f"Scraping error: {e.message}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ========== Analyze Endpoints (Return JSON) ==========

@router.post(
    "/analyze/single",
    response_model=ProcessingResponse,
    tags=["Requirements Extraction"],
    summary="Analyze single comment and return JSON"
)
async def analyze_single_comment(request: SingleCommentRequest):
    """
    Analyze a single comment and return JSON results (no PDF)

    Args:
        request: Single comment request

    Returns:
        JSON with requirement analysis results
    """
    try:
        logger.info(f"Analyzing single comment: {request.comment[:100]}...")

        # Process and get response
        response, _ = await orchestrator_service.process_single_comment(request.comment)

        return response

    except PerseusException as e:
        logger.error(f"Processing error: {e.message}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/analyze/csv",
    response_model=ProcessingResponse,
    tags=["Requirements Extraction"],
    summary="Analyze CSV file and return JSON"
)
async def analyze_csv_file(file: UploadFile = File(...)):
    """
    Analyze CSV file and return JSON results (no PDF)

    Args:
        file: Uploaded CSV file

    Returns:
        JSON with requirement analysis results
    """
    try:
        logger.info(f"Analyzing CSV file: {file.filename}")

        # Validate file extension
        if not file.filename.endswith('.csv'):
            raise ValidationException("File must be a CSV file")

        # Process and get response
        response, _ = await orchestrator_service.process_csv_file(file)

        return response

    except FileProcessingException as e:
        logger.error(f"File processing error: {e.message}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post(
    "/analyze/playstore",
    response_model=ProcessingResponse,
    tags=["Requirements Extraction"],
    summary="Analyze Play Store URL with smart scraping and return JSON"
)
async def analyze_playstore_url(request: PlayStoreURLRequest):
    """
    Analyze Google Play Store URL with intelligent filtering and return JSON results

    Smart scraping filters:
    - Rating: 2-3 stars (critical feedback)
    - Minimum: 15+ words per comment
    - Target: 30 valid requirements
    - Maximum: 500 reviews analyzed

    Returns detailed statistics including:
    - total_scraped: Total reviews checked
    - valid_comments: Comments that passed filters
    - filtered_by_rating: Comments filtered by rating
    - filtered_by_words: Comments filtered by word count

    Args:
        request: Play Store URL request

    Returns:
        JSON with requirement analysis results and scraping statistics
    """
    try:
        logger.info(f"Analyzing Play Store URL with smart scraping: {request.url}")

        # Process with smart scraping
        response, _ = await orchestrator_service.process_playstore_url(
            request.url,
            target_requirements=30,
            max_total_reviews=500
        )

        return response

    except ScrapingException as e:
        logger.error(f"Scraping error: {e.message}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except ValidationException as e:
        logger.error(f"Validation error: {e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
