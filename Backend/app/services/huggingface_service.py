"""
HuggingFace Model Service
Handles loading and inference of HuggingFace transformer models
"""

from typing import Dict, List, Optional
from transformers import pipeline, Pipeline
import torch
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import ModelLoadException, PredictionException
from app.core.constants import PIPELINE_TASK

logger = get_logger(__name__)


class HuggingFaceService:
    """
    Service for managing HuggingFace models
    Singleton pattern to avoid loading models multiple times
    """

    _instance: Optional['HuggingFaceService'] = None
    _binary_pipeline: Optional[Pipeline] = None
    _multiclass_pipeline: Optional[Pipeline] = None

    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super(HuggingFaceService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize service (only once due to singleton)"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            logger.info("Initializing HuggingFace Service")

    @property
    def binary_pipeline(self) -> Pipeline:
        """Get or load binary classification pipeline"""
        if self._binary_pipeline is None:
            self._binary_pipeline = self._load_model(
                settings.BINARY_MODEL_NAME,
                "binary"
            )
        return self._binary_pipeline

    @property
    def multiclass_pipeline(self) -> Pipeline:
        """Get or load multiclass classification pipeline"""
        if self._multiclass_pipeline is None:
            self._multiclass_pipeline = self._load_model(
                settings.MULTICLASS_MODEL_NAME,
                "multiclass"
            )
        return self._multiclass_pipeline

    def _load_model(self, model_name: str, model_type: str) -> Pipeline:
        """
        Load a HuggingFace model pipeline

        Args:
            model_name: Model identifier on HuggingFace Hub
            model_type: Type of model (binary/multiclass) for logging

        Returns:
            Loaded pipeline

        Raises:
            ModelLoadException: If model fails to load
        """
        try:
            logger.info(f"Loading {model_type} model: {model_name}")

            # Determine device
            device = 0 if torch.cuda.is_available() else -1
            device_name = "CUDA" if device == 0 else "CPU"

            logger.info(f"Using device: {device_name}")

            # Load pipeline with truncation to handle long sequences
            pipe = pipeline(
                PIPELINE_TASK,
                model=model_name,
                device=device,
                token=settings.HUGGINGFACE_TOKEN,
                truncation=True,
                max_length=512
            )

            logger.info(f"{model_type.capitalize()} model loaded successfully")
            return pipe

        except Exception as e:
            error_msg = f"Failed to load {model_type} model '{model_name}': {str(e)}"
            logger.error(error_msg)
            raise ModelLoadException(error_msg, details={"model": model_name, "error": str(e)})

    def predict_binary(self, text: str) -> Dict:
        """
        Predict if text is a valid requirement (binary classification)

        Args:
            text: Input text to classify

        Returns:
            Dictionary with label and score

        Raises:
            PredictionException: If prediction fails
        """
        try:
            result = self.binary_pipeline(text)[0]
            logger.debug(f"Binary prediction for '{text[:50]}...': {result}")
            return result

        except Exception as e:
            error_msg = f"Binary prediction failed: {str(e)}"
            logger.error(error_msg)
            raise PredictionException(error_msg, details={"text": text[:100]})

    def predict_multiclass(self, text: str) -> Dict:
        """
        Predict security subcharacteristic (multiclass classification)

        Args:
            text: Input text to classify

        Returns:
            Dictionary with label and score

        Raises:
            PredictionException: If prediction fails
        """
        try:
            result = self.multiclass_pipeline(text)[0]
            logger.debug(f"Multiclass prediction for '{text[:50]}...': {result}")
            return result

        except Exception as e:
            error_msg = f"Multiclass prediction failed: {str(e)}"
            logger.error(error_msg)
            raise PredictionException(error_msg, details={"text": text[:100]})

    def batch_predict_binary(self, texts: List[str]) -> List[Dict]:
        """
        Batch predict for multiple texts (binary)

        Args:
            texts: List of texts to classify

        Returns:
            List of prediction dictionaries
        """
        try:
            results = self.binary_pipeline(texts)
            # Handle both single result and batch results
            if isinstance(results[0], list):
                return [r[0] for r in results]
            return results

        except Exception as e:
            error_msg = f"Batch binary prediction failed: {str(e)}"
            logger.error(error_msg)
            raise PredictionException(error_msg)

    def batch_predict_multiclass(self, texts: List[str]) -> List[Dict]:
        """
        Batch predict for multiple texts (multiclass)

        Args:
            texts: List of texts to classify

        Returns:
            List of prediction dictionaries
        """
        try:
            results = self.multiclass_pipeline(texts)
            # Handle both single result and batch results
            if isinstance(results[0], list):
                return [r[0] for r in results]
            return results

        except Exception as e:
            error_msg = f"Batch multiclass prediction failed: {str(e)}"
            logger.error(error_msg)
            raise PredictionException(error_msg)

    def is_loaded(self) -> Dict[str, bool]:
        """
        Check if models are loaded

        Returns:
            Dictionary with load status of each model
        """
        return {
            "binary": self._binary_pipeline is not None,
            "multiclass": self._multiclass_pipeline is not None
        }

    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about loaded models

        Returns:
            Dictionary with model names
        """
        return {
            "binary_model": settings.BINARY_MODEL_NAME,
            "multiclass_model": settings.MULTICLASS_MODEL_NAME
        }


# Global service instance
huggingface_service = HuggingFaceService()
