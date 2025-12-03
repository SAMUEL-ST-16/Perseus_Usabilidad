"""
Processing Service
Handles the core logic of processing comments and extracting requirements
"""

import asyncio
from typing import List, Dict
from app.services.huggingface_service import huggingface_service
from app.schemas.requirements import BinaryPrediction, MulticlassPrediction, CommentAnalysis
from app.schemas.models import RequirementResult
from app.core.logger import get_logger
from app.core.constants import BINARY_VALID_LABELS, BINARY_INVALID_LABELS

logger = get_logger(__name__)


class ProcessingService:
    """
    Service for processing comments and classifying requirements
    """

    def __init__(self):
        """Initialize processing service"""
        logger.info("Initializing Processing Service")

    def _is_valid_requirement(self, label: str) -> bool:
        """
        Determine if a binary prediction label indicates a valid requirement

        Args:
            label: Prediction label from binary model

        Returns:
            True if it's a valid requirement, False otherwise
        """
        # Check if label indicates valid requirement
        if label in BINARY_VALID_LABELS:
            return True
        elif label in BINARY_INVALID_LABELS:
            return False
        else:
            # Unknown label - log warning and default to False
            logger.warning(f"Unknown binary label: {label}. Defaulting to not a requirement.")
            return False

    async def process_single_comment(
        self,
        comment: str,
        generate_description: bool = True
    ) -> CommentAnalysis:
        """
        Process a single comment through binary and multiclass classification - ASYNC

        Args:
            comment: Comment text to process
            generate_description: Whether to generate description for requirements

        Returns:
            CommentAnalysis with predictions
        """
        logger.info(f"Processing comment: {comment[:100]}...")

        # Step 1: Binary classification (run in thread pool as it's CPU-bound)
        loop = asyncio.get_event_loop()
        binary_result = await loop.run_in_executor(
            None,
            huggingface_service.predict_binary,
            comment
        )
        is_requirement = self._is_valid_requirement(binary_result['label'])

        binary_prediction = BinaryPrediction(
            label=binary_result['label'],
            score=binary_result['score'],
            is_requirement=is_requirement
        )

        logger.info(f"Binary result: {binary_result['label']} (score: {binary_result['score']:.4f})")

        # Step 2: If it's a requirement, classify subcharacteristic
        multiclass_prediction = None
        description = None

        if is_requirement:
            multiclass_result = await loop.run_in_executor(
                None,
                huggingface_service.predict_multiclass,
                comment
            )
            multiclass_prediction = MulticlassPrediction(
                label=multiclass_result['label'],
                score=multiclass_result['score']
            )

            logger.info(
                f"Multiclass result: {multiclass_result['label']} "
                f"(score: {multiclass_result['score']:.4f})"
            )

            # Step 3: Generate description if requested (ASYNC)
            if generate_description:
                from app.services.description_service import description_service
                description = await description_service.generate_description(
                    comment=comment,
                    subcharacteristic=multiclass_result['label']
                )

        return CommentAnalysis(
            comment=comment,
            binary_prediction=binary_prediction,
            multiclass_prediction=multiclass_prediction,
            description=description
        )

    async def process_batch(
        self,
        comments: List[str],
        generate_descriptions: bool = True
    ) -> List[RequirementResult]:
        """
        Process multiple comments efficiently with PARALLEL LLM calls - ASYNC

        Args:
            comments: List of comment texts
            generate_descriptions: Whether to generate descriptions

        Returns:
            List of RequirementResult objects
        """
        logger.info(f"Processing batch of {len(comments)} comments")

        if not comments:
            return []

        # Step 1: Binary classification for all comments (run in thread pool)
        loop = asyncio.get_event_loop()
        binary_results = await loop.run_in_executor(
            None,
            huggingface_service.batch_predict_binary,
            comments
        )

        # Step 2: Filter valid requirements
        valid_indices = []
        valid_comments = []

        for idx, (comment, binary_result) in enumerate(zip(comments, binary_results)):
            if self._is_valid_requirement(binary_result['label']):
                valid_indices.append(idx)
                valid_comments.append(comment)

        logger.info(f"Found {len(valid_comments)} valid requirements out of {len(comments)}")

        # Step 3: Multiclass classification for valid requirements (run in thread pool)
        multiclass_results = []
        if valid_comments:
            multiclass_results = await loop.run_in_executor(
                None,
                huggingface_service.batch_predict_multiclass,
                valid_comments
            )

        # Step 4: Generate descriptions if requested - PARALLEL EXECUTION ⚡
        descriptions = []
        if generate_descriptions and valid_comments:
            from app.services.description_service import description_service

            logger.info(f"🚀 Generating {len(valid_comments)} descriptions in PARALLEL...")

            # Create tasks for parallel execution
            description_tasks = [
                description_service.generate_description(
                    comment=comment,
                    subcharacteristic=mc_result['label']
                )
                for comment, mc_result in zip(valid_comments, multiclass_results)
            ]

            # Execute all LLM calls in parallel
            descriptions = await asyncio.gather(*description_tasks)

            logger.info(f"✓ Generated {len(descriptions)} descriptions in parallel")

        # Step 5: Build final results
        results = []
        multiclass_idx = 0

        for idx, (comment, binary_result) in enumerate(zip(comments, binary_results)):
            is_requirement = self._is_valid_requirement(binary_result['label'])

            if is_requirement and multiclass_idx < len(multiclass_results):
                # Valid requirement with multiclass classification
                mc_result = multiclass_results[multiclass_idx]
                desc = descriptions[multiclass_idx] if descriptions else None

                results.append(RequirementResult(
                    comment=comment,
                    is_requirement=True,
                    subcharacteristic=mc_result['label'],
                    description=desc,
                    binary_score=binary_result['score'],
                    multiclass_score=mc_result['score']
                ))
                multiclass_idx += 1
            else:
                # Not a requirement
                results.append(RequirementResult(
                    comment=comment,
                    is_requirement=False,
                    subcharacteristic=None,
                    description=None,
                    binary_score=binary_result['score'],
                    multiclass_score=None
                ))

        return results


# Global service instance
processing_service = ProcessingService()
