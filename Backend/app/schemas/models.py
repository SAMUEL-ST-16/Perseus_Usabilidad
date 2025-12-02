"""
Pydantic models for Perseus Backend
Defines request/response schemas for API endpoints
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class UsabilitySubcharacteristic(str, Enum):
    """
    ISO 25010:2023 Usability Subcharacteristics
    """
    OPERABILIDAD = "Operabilidad"
    APRENDIZABILIDAD = "Aprendizabilidad"
    INVOLUCRACION = "Involucración del usuario"
    RECONOCIBILIDAD = "Reconocibilidad de adecuación"
    PROTECCION_ERRORES = "Protección frente a errores de usuario"
    INCLUSIVIDAD = "Inclusividad"
    AUTO_DESCRIPTIVIDAD = "Auto descriptividad"
    ASISTENCIA = "Asistencia al usuario"


# ========== Request Models ==========

class SingleCommentRequest(BaseModel):
    """Request for processing a single comment"""
    comment: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User comment to analyze"
    )

    @validator('comment')
    def validate_comment(cls, v):
        """Validate comment is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError("Comment cannot be empty or whitespace only")
        return v.strip()


class PlayStoreURLRequest(BaseModel):
    """Request for processing Google Play Store URL"""
    url: str = Field(
        ...,
        description="Google Play Store app URL"
    )

    @validator('url')
    def validate_playstore_url(cls, v):
        """Validate URL is a valid Play Store URL"""
        if not v or not v.strip():
            raise ValueError("URL cannot be empty")

        v = v.strip()

        # Check if it's a valid Play Store URL
        valid_patterns = [
            "play.google.com/store/apps/details",
            "market://details?id="
        ]

        if not any(pattern in v for pattern in valid_patterns):
            raise ValueError(
                "Invalid Play Store URL. Must contain 'play.google.com/store/apps/details'"
            )

        return v


# ========== Response Models ==========

class RequirementResult(BaseModel):
    """Individual requirement analysis result"""
    comment: str = Field(..., description="Original comment text")
    is_requirement: bool = Field(..., description="Whether it's a valid requirement")
    subcharacteristic: Optional[str] = Field(
        None,
        description="Usability subcharacteristic according to ISO 25010:2023 (if valid requirement)"
    )
    description: Optional[str] = Field(
        None,
        description="Generated description (if valid requirement)"
    )
    binary_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Binary classification confidence score"
    )
    multiclass_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Multiclass classification confidence score"
    )


class ProcessingResponse(BaseModel):
    """Complete processing response with all results"""
    total_comments: int = Field(..., description="Total number of comments processed")
    valid_requirements: int = Field(..., description="Number of valid requirements found")
    requirements: List[RequirementResult] = Field(
        default_factory=list,
        description="List of requirement analysis results"
    )
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    source_type: Literal["single", "csv", "playstore"] = Field(
        ...,
        description="Source type of the comments"
    )
    scraping_stats: Optional[dict] = Field(
        None,
        description="Scraping statistics (only for playstore source)"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    binary_model_loaded: bool = Field(..., description="Binary model load status")
    multiclass_model_loaded: bool = Field(..., description="Multiclass model load status")
    binary_model_name: str = Field(..., description="Binary model identifier")
    multiclass_model_name: str = Field(..., description="Multiclass model identifier")


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")


# ========== Processing Statistics ==========

class ProcessingStats(BaseModel):
    """Statistics for Play Store processing"""
    comments_processed: int = Field(..., description="Total comments scraped")
    requirements_found: int = Field(..., description="Valid requirements detected")
    total_requirements_detected: int = Field(..., description="Total requirements found")
    success_rate: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Success rate percentage"
    )
    target: int = Field(..., description="Target number of comments to scrape")
