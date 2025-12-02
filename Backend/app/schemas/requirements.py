"""
Additional schema definitions for requirements processing
"""

from typing import Optional
from pydantic import BaseModel, Field


class BinaryPrediction(BaseModel):
    """Result of binary classification (is it a requirement?)"""
    label: str = Field(..., description="Predicted label")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    is_requirement: bool = Field(..., description="Whether it's a valid requirement")


class MulticlassPrediction(BaseModel):
    """Result of multiclass classification (which subcharacteristic?)"""
    label: str = Field(..., description="Predicted security subcharacteristic")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class CommentAnalysis(BaseModel):
    """Complete analysis of a single comment"""
    comment: str = Field(..., description="Original comment text")
    binary_prediction: BinaryPrediction = Field(..., description="Binary classification result")
    multiclass_prediction: Optional[MulticlassPrediction] = Field(
        None,
        description="Multiclass classification result (only if valid requirement)"
    )
    description: Optional[str] = Field(
        None,
        description="Generated description (only if valid requirement)"
    )


class CSVRow(BaseModel):
    """Represents a row from CSV file"""
    comment: str = Field(..., description="Comment text from CSV")
    row_number: int = Field(..., description="Row number in CSV file")


class ScrapedComment(BaseModel):
    """Represents a scraped comment from Play Store"""
    text: str = Field(..., description="Comment text")
    author: Optional[str] = Field(None, description="Comment author")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Star rating")
    date: Optional[str] = Field(None, description="Comment date")
