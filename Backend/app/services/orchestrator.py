"""
Orchestrator Service
Coordinates all services to process requirements end-to-end
"""

import time
import csv
from io import StringIO, BytesIO
from typing import List, Tuple
from fastapi import UploadFile
from app.services.processing_service import processing_service
from app.services.scraper_service import scraper_service
from app.services.pdf_service import pdf_service
from app.schemas.models import ProcessingResponse, RequirementResult
from app.core.logger import get_logger
from app.core.exceptions import FileProcessingException

logger = get_logger(__name__)


class OrchestratorService:
    """
    Orchestrates the complete workflow of requirement extraction
    """

    def __init__(self):
        """Initialize orchestrator service"""
        logger.info("Initializing Orchestrator Service")

    async def process_single_comment(
        self,
        comment: str
    ) -> Tuple[ProcessingResponse, BytesIO]:
        """
        Process a single comment and generate both JSON and PDF

        Args:
            comment: User comment

        Returns:
            Tuple of (ProcessingResponse, PDF buffer)
        """
        logger.info("Orchestrating single comment processing")
        start_time = time.time()

        # Process comment (ASYNC)
        results = await processing_service.process_batch([comment], generate_descriptions=True)

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # Build response
        response = ProcessingResponse(
            total_comments=1,
            valid_requirements=sum(1 for r in results if r.is_requirement),
            requirements=results,
            processing_time_ms=processing_time_ms,
            source_type="single"
        )

        # Generate PDF
        pdf_buffer = pdf_service.generate_pdf(response)

        logger.info(f"Single comment processed in {processing_time_ms:.2f}ms")

        return response, pdf_buffer

    async def process_csv_file(
        self,
        file: UploadFile
    ) -> Tuple[ProcessingResponse, BytesIO]:
        """
        Process CSV file with multiple comments

        Args:
            file: Uploaded CSV file

        Returns:
            Tuple of (ProcessingResponse, PDF buffer)

        Raises:
            FileProcessingException: If CSV processing fails
        """
        logger.info(f"Orchestrating CSV file processing: {file.filename}")
        start_time = time.time()

        try:
            # Read CSV file
            contents = await file.read()

            # Try multiple encodings
            csv_text = None
            encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1', 'cp1252']

            for encoding in encodings:
                try:
                    csv_text = contents.decode(encoding)
                    logger.info(f"Successfully decoded CSV with encoding: {encoding}")
                    break
                except UnicodeDecodeError:
                    continue

            if csv_text is None:
                raise FileProcessingException(
                    "Could not decode CSV file. Please ensure file is in UTF-8, Latin-1, or Windows-1252 encoding."
                )

            # Parse CSV
            comments = self._parse_csv(csv_text)

            logger.info(f"Extracted {len(comments)} comments from CSV")

            # Process all comments (ASYNC)
            results = await processing_service.process_batch(comments, generate_descriptions=True)

            # Calculate processing time
            processing_time_ms = (time.time() - start_time) * 1000

            # Build response
            response = ProcessingResponse(
                total_comments=len(comments),
                valid_requirements=sum(1 for r in results if r.is_requirement),
                requirements=results,
                processing_time_ms=processing_time_ms,
                source_type="csv"
            )

            # Generate PDF
            pdf_buffer = pdf_service.generate_pdf(response)

            logger.info(f"CSV processed in {processing_time_ms:.2f}ms")

            return response, pdf_buffer

        except Exception as e:
            error_msg = f"Failed to process CSV file: {str(e)}"
            logger.error(error_msg)
            raise FileProcessingException(error_msg, details={"filename": file.filename})

    async def process_playstore_url(
        self,
        url: str,
        target_requirements: int = 30,
        max_total_reviews: int = 500
    ) -> Tuple[ProcessingResponse, BytesIO]:
        """
        Smart processing of Google Play Store URL

        Strategy:
        1. Scrape comments with quality filters (2-3 stars, 15+ words)
        2. Process progressively until finding target_requirements valid requirements
        3. Stop if max_total_reviews is reached
        4. Return detailed statistics

        Args:
            url: Play Store app URL
            target_requirements: Target number of valid requirements (default: 30)
            max_total_reviews: Maximum total reviews to scrape (default: 500)

        Returns:
            Tuple of (ProcessingResponse, PDF buffer)
        """
        logger.info(f"Orchestrating Smart Play Store processing: {url}")
        logger.info(f"Target: {target_requirements} requirements, Max: {max_total_reviews} reviews")
        start_time = time.time()

        # Smart scraping with filters (ASYNC)
        comments, scraping_stats = await scraper_service.get_comments_only_smart(
            url,
            target_comments=target_requirements,  # Scrape enough filtered comments
            max_total=max_total_reviews
        )

        logger.info(f"Smart scraping completed: {scraping_stats}")
        logger.info(f"Processing {len(comments)} filtered comments...")

        # Process all filtered comments to find requirements (ASYNC)
        results = await processing_service.process_batch(comments, generate_descriptions=True)

        # Get valid requirements
        valid_requirements = [r for r in results if r.is_requirement]

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # Build response with enhanced statistics
        response = ProcessingResponse(
            total_comments=scraping_stats["total_scraped"],  # Total reviews checked
            valid_requirements=len(valid_requirements),
            requirements=results,  # All processed results
            processing_time_ms=processing_time_ms,
            source_type="playstore"
        )

        # Add scraping statistics to response (for frontend display)
        response.scraping_stats = scraping_stats

        # Generate PDF
        pdf_buffer = pdf_service.generate_pdf(response)

        logger.info(
            f"✓ Play Store processing completed: "
            f"{len(valid_requirements)} requirements found from "
            f"{scraping_stats['total_scraped']} reviews in {processing_time_ms:.2f}ms"
        )

        return response, pdf_buffer

    def _parse_csv(self, csv_text: str) -> List[str]:
        """
        Parse CSV text and extract comments

        Args:
            csv_text: CSV file content as string

        Returns:
            List of comment strings

        Raises:
            FileProcessingException: If CSV parsing fails
        """
        try:
            # Create CSV reader
            csv_file = StringIO(csv_text)
            reader = csv.reader(csv_file)

            # Skip header if present
            first_row = next(reader, None)
            if first_row is None:
                raise FileProcessingException("CSV file is empty")

            comments = []

            # Check if first row is header or data
            # Simple heuristic: if first cell contains "comment" or "text", treat as header
            first_cell = first_row[0].lower() if first_row else ""
            is_header = any(word in first_cell for word in ['comment', 'text', 'review', 'comentario'])

            if not is_header:
                # First row is data, include it
                if first_row and first_row[0].strip():
                    comments.append(first_row[0].strip())

            # Read remaining rows
            for row in reader:
                if row and row[0].strip():
                    comments.append(row[0].strip())

            if not comments:
                raise FileProcessingException("No valid comments found in CSV")

            logger.info(f"Parsed {len(comments)} comments from CSV")
            return comments

        except FileProcessingException:
            raise
        except Exception as e:
            raise FileProcessingException(
                f"Failed to parse CSV: {str(e)}",
                details={"error": str(e)}
            )


# Global service instance
orchestrator_service = OrchestratorService()
