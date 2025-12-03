"""
Scraper Service
Handles web scraping of Google Play Store reviews with intelligent filtering
"""

import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Dict, Tuple
from google_play_scraper import reviews, Sort
from app.schemas.requirements import ScrapedComment
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import ScrapingException

logger = get_logger(__name__)


class ScraperService:
    """
    Service for scraping Google Play Store reviews with intelligent filtering

    Filters applied:
    - Rating: 2-3 stars (critical but not extreme)
    - Minimum words: 15+ words per comment
    - Smart limits: Max 30 valid requirements, max 500 comments reviewed
    """

    # Quality filters
    MIN_RATING = 2
    MAX_RATING = 3
    MIN_WORDS = 15

    def __init__(self):
        """Initialize scraper service"""
        logger.info("Initializing Scraper Service with intelligent filtering")
        logger.info(f"Filters: Rating {self.MIN_RATING}-{self.MAX_RATING} stars, Min {self.MIN_WORDS} words")
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _extract_app_id(self, url: str) -> str:
        """
        Extract app ID from Play Store URL

        Args:
            url: Play Store URL

        Returns:
            App ID (package name)

        Raises:
            ScrapingException: If app ID cannot be extracted
        """
        # Pattern: play.google.com/store/apps/details?id=PACKAGE_NAME
        patterns = [
            r'id=([a-zA-Z0-9._]+)',  # From URL
            r'details\?id=([a-zA-Z0-9._]+)',  # Alternative pattern
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                app_id = match.group(1)
                logger.info(f"Extracted app ID: {app_id}")
                return app_id

        raise ScrapingException(
            f"Could not extract app ID from URL: {url}",
            details={"url": url}
        )

    def _count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.split())

    def _is_valid_comment(self, comment: ScrapedComment) -> bool:
        """
        Check if comment meets quality criteria

        Args:
            comment: Scraped comment to validate

        Returns:
            True if comment is valid, False otherwise
        """
        # Check if text exists
        if not comment.text or not comment.text.strip():
            return False

        # Check rating (2-3 stars)
        if comment.rating is None or comment.rating < self.MIN_RATING or comment.rating > self.MAX_RATING:
            return False

        # Check minimum words
        word_count = self._count_words(comment.text)
        if word_count < self.MIN_WORDS:
            return False

        return True

    def _scrape_reviews_smart_sync(
        self,
        url: str,
        target_valid_comments: int = 30,
        max_total_reviews: int = 500,
        language: str = 'es',
        country: str = 'us'
    ) -> Tuple[List[ScrapedComment], Dict]:
        """
        Synchronous version of smart scraping (to run in executor)

        Args:
            url: Play Store app URL
            target_valid_comments: Target number of valid comments (default: 30)
            max_total_reviews: Maximum reviews to scrape (default: 500)
            language: Review language filter
            country: Country filter

        Returns:
            Tuple of (valid_comments, statistics)

        Raises:
            ScrapingException: If scraping fails
        """
        try:
            app_id = self._extract_app_id(url)

            logger.info(f"Smart scraping started for app: {app_id}")
            logger.info(f"Target: {target_valid_comments} valid comments, Max: {max_total_reviews} total")

            valid_comments = []
            total_scraped = 0
            filtered_by_rating = 0
            filtered_by_words = 0
            batch_size = 100  # Scrape in batches

            continuation_token = None

            while len(valid_comments) < target_valid_comments and total_scraped < max_total_reviews:
                # Calculate how many more to scrape
                remaining = max_total_reviews - total_scraped
                current_batch = min(batch_size, remaining)

                logger.info(f"Scraping batch of {current_batch} reviews... (Total so far: {total_scraped})")

                # Scrape batch
                result, continuation_token = reviews(
                    app_id,
                    lang=language,
                    country=country,
                    sort=Sort.MOST_RELEVANT,
                    count=current_batch,
                    continuation_token=continuation_token
                )

                if not result:
                    logger.warning("No more reviews available")
                    break

                # Process batch
                for review in result:
                    total_scraped += 1

                    comment = ScrapedComment(
                        text=review.get('content', ''),
                        author=review.get('userName', None),
                        rating=review.get('score', None),
                        date=str(review.get('at', None))
                    )

                    # Apply filters
                    if not comment.text or not comment.text.strip():
                        continue

                    if comment.rating is None or comment.rating < self.MIN_RATING or comment.rating > self.MAX_RATING:
                        filtered_by_rating += 1
                        continue

                    word_count = self._count_words(comment.text)
                    if word_count < self.MIN_WORDS:
                        filtered_by_words += 1
                        continue

                    # Valid comment!
                    valid_comments.append(comment)

                    # Check if we reached target
                    if len(valid_comments) >= target_valid_comments:
                        logger.info(f"✓ Target reached! Found {len(valid_comments)} valid comments")
                        break

                logger.info(f"Valid comments so far: {len(valid_comments)}/{target_valid_comments}")

                # Check if continuation token exists
                if not continuation_token:
                    logger.warning("No more reviews available from API")
                    break

            # Build statistics
            stats = {
                "total_scraped": total_scraped,
                "valid_comments": len(valid_comments),
                "filtered_by_rating": filtered_by_rating,
                "filtered_by_words": filtered_by_words,
                "filtered_empty": total_scraped - len(valid_comments) - filtered_by_rating - filtered_by_words,
                "target_reached": len(valid_comments) >= target_valid_comments,
                "max_limit_reached": total_scraped >= max_total_reviews
            }

            logger.info(f"Smart scraping completed: {stats}")

            return valid_comments, stats

        except ScrapingException:
            raise
        except Exception as e:
            error_msg = f"Failed to scrape reviews from {url}: {str(e)}"
            logger.error(error_msg)
            raise ScrapingException(error_msg, details={"url": url, "error": str(e)})

    async def scrape_reviews_smart(
        self,
        url: str,
        target_valid_comments: int = 30,
        max_total_reviews: int = 500,
        language: str = 'es',
        country: str = 'us'
    ) -> Tuple[List[ScrapedComment], Dict]:
        """
        Smart scraping with progressive filtering - ASYNC with CACHE

        Stops when:
        - Found target_valid_comments that meet criteria
        - OR reached max_total_reviews

        Args:
            url: Play Store app URL
            target_valid_comments: Target number of valid comments (default: 30)
            max_total_reviews: Maximum reviews to scrape (default: 500)
            language: Review language filter
            country: Country filter

        Returns:
            Tuple of (valid_comments, statistics)

        Raises:
            ScrapingException: If scraping fails
        """
        from app.services.redis_service import redis_service

        # Extract app_id for caching
        app_id = self._extract_app_id(url)

        # Try cache first
        cache_key = redis_service._generate_key(
            "scraping",
            app_id,
            target_valid_comments,
            max_total_reviews,
            language,
            country
        )
        cached = await redis_service.get(cache_key)
        if cached is not None:
            logger.info(f"🎯 Cache HIT for scraping: {app_id}")
            # Reconstruct ScrapedComment objects from cached data
            comments = [ScrapedComment(**c) for c in cached['comments']]
            return comments, cached['stats']

        # Run blocking scraping in executor
        loop = asyncio.get_event_loop()
        valid_comments, stats = await loop.run_in_executor(
            self.executor,
            self._scrape_reviews_smart_sync,
            url,
            target_valid_comments,
            max_total_reviews,
            language,
            country
        )

        # Cache the result (convert to dict for JSON serialization)
        cache_data = {
            'comments': [c.model_dump() for c in valid_comments],
            'stats': stats
        }
        await redis_service.set(cache_key, cache_data, ttl=settings.CACHE_TTL_SCRAPING)

        return valid_comments, stats

    async def get_comments_only_smart(
        self,
        url: str,
        target_comments: int = 30,
        max_total: int = 500
    ) -> Tuple[List[str], Dict]:
        """
        Smart scraping that returns only comment texts with statistics - ASYNC

        Args:
            url: Play Store app URL
            target_comments: Target number of valid comments
            max_total: Maximum total reviews to scrape

        Returns:
            Tuple of (comment_texts, statistics)
        """
        valid_comments, stats = await self.scrape_reviews_smart(
            url,
            target_valid_comments=target_comments,
            max_total_reviews=max_total
        )
        comment_texts = [comment.text for comment in valid_comments]
        return comment_texts, stats


# Global service instance
scraper_service = ScraperService()
