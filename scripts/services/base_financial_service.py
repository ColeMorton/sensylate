"""
Base Financial Service

Provides common infrastructure for all financial data services including:
- Standardized error handling and validation
- Production-grade caching with TTL support
- Rate limiting with service-specific limits
- Logging with correlation IDs
- Configuration management
- Data validation with Pydantic models
"""

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from pydantic import BaseModel, Field


class FinancialServiceError(Exception):
    """Base exception for financial service errors"""

    pass


class ValidationError(FinancialServiceError):
    """Raised when input validation fails"""

    pass


class RateLimitError(FinancialServiceError):
    """Raised when rate limit is exceeded"""

    pass


class DataNotFoundError(FinancialServiceError):
    """Raised when requested data is not available"""

    pass


class APITimeoutError(FinancialServiceError):
    """Raised when API request times out"""

    pass


class CacheConfig(BaseModel):
    """Cache configuration"""

    enabled: bool = True
    ttl_seconds: int = 900  # 15 minutes default
    cache_dir: str = Field(default_factory=lambda: str(Path.cwd() / "data" / "cache"))
    max_size_mb: int = 100


class RateLimitConfig(BaseModel):
    """Rate limiting configuration"""

    enabled: bool = True
    requests_per_minute: int = 60
    burst_limit: int = 10


class ServiceConfig(BaseModel):
    """Base service configuration"""

    name: str
    base_url: str
    api_key: Optional[str] = None
    timeout_seconds: int = 30
    max_retries: int = 3
    cache: CacheConfig = Field(default_factory=CacheConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    headers: Dict[str, str] = Field(default_factory=dict)


class FileBasedCache:
    """Production-grade file-based cache with TTL support"""

    def __init__(self, config: CacheConfig, service_name: str = "unknown"):
        self.config = config
        self.service_name = service_name
        self.cache_dir = Path(config.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Generate cache file path for given key - consistent with UnifiedCacheManager"""
        # Use consistent cache key generation across all cache implementations
        hash_key = hashlib.md5(f"{self.service_name}_{key}".encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.json"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached data if not expired"""
        if not self.config.enabled:
            return None

        cache_path = self._get_cache_path(key)
        if not cache_path.exists():
            return None

        try:
            with open(cache_path, "r") as f:
                cached_data = json.load(f)

            # Check if cache is expired
            cached_time = datetime.fromisoformat(cached_data["timestamp"])
            if datetime.now() - cached_time > timedelta(
                seconds=self.config.ttl_seconds
            ):
                cache_path.unlink()  # Remove expired cache
                return None

            return cached_data["data"]

        except (json.JSONDecodeError, KeyError, ValueError):
            # Remove corrupted cache file
            cache_path.unlink(missing_ok=True)
            return None

    def set(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in cache with timestamp"""
        if not self.config.enabled:
            return

        cache_path = self._get_cache_path(key)
        cached_data = {"timestamp": datetime.now().isoformat(), "data": data}

        try:
            with open(cache_path, "w") as f:
                json.dump(cached_data, f, default=str)
        except Exception as e:
            logging.warning(f"Failed to write cache: {e}")

    def clear(self) -> None:
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink(missing_ok=True)

    def cleanup_expired(self) -> None:
        """Remove expired cache entries"""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)
                cached_time = datetime.fromisoformat(cached_data["timestamp"])
                if datetime.now() - cached_time > timedelta(
                    seconds=self.config.ttl_seconds
                ):
                    cache_file.unlink()
            except Exception:
                # Remove corrupted files
                cache_file.unlink(missing_ok=True)


class RateLimiter:
    """Production-grade rate limiter with burst support"""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.requests: List[float] = []

    def can_make_request(self) -> bool:
        """Check if request is allowed under rate limit"""
        if not self.config.enabled:
            return True

        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]

        return len(self.requests) < self.config.requests_per_minute

    def record_request(self) -> None:
        """Record a new request"""
        if self.config.enabled:
            self.requests.append(time.time())

    def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded"""
        if not self.config.enabled:
            return

        if not self.can_make_request():
            # Calculate wait time until oldest request expires
            oldest_request = min(self.requests)
            wait_time = 60 - (time.time() - oldest_request) + 1
            if wait_time > 0:
                time.sleep(wait_time)


class BaseFinancialService(ABC):
    """
    Base class for all financial data services

    Provides common infrastructure including:
    - Caching with TTL
    - Rate limiting
    - Error handling with retry logic
    - Request logging with correlation IDs
    - Data validation
    """

    def __init__(self, config: ServiceConfig):
        self.config = config
        self.cache = FileBasedCache(config.cache, config.name)
        self.rate_limiter = RateLimiter(config.rate_limit)
        self.session = requests.Session()
        self.logger = self._setup_logger()

        # Update session headers
        self.session.headers.update(
            {
                "User-Agent": "Sensylate/1.0 (https://sensylate.com)",
                "Accept": "application/json",
                **config.headers,
            }
        )

    def _setup_logger(self) -> logging.Logger:
        """Setup structured logging for the service"""
        logger = logging.getLogger(f"financial_service.{self.config.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _generate_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache key from endpoint and parameters"""
        cache_data = (
            f"{self.config.name}_{endpoint}_{json.dumps(params, sort_keys=True)}"
        )
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _generate_correlation_id(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate correlation ID for request tracking"""
        correlation_data = f"{endpoint}_{params}_{time.time()}"
        return hashlib.md5(correlation_data.encode()).hexdigest()[:8]

    def _make_request_with_retry(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        cache_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Make API request with caching, rate limiting, and retry logic

        Args:
            endpoint: API endpoint to call
            params: Request parameters
            cache_key: Optional custom cache key

        Returns:
            API response data

        Raises:
            RateLimitError: When rate limit is exceeded
            DataNotFoundError: When requested data is not available
            APITimeoutError: When request times out
            FinancialServiceError: For other API errors
        """
        if params is None:
            params = {}

        # Generate cache key and correlation ID
        if cache_key is None:
            cache_key = self._generate_cache_key(endpoint, params)
        correlation_id = self._generate_correlation_id(endpoint, params)

        # Check cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            self.logger.info(f"Cache hit for {endpoint} - ID: {correlation_id}")
            return cached_data

        # Prepare request parameters
        if self.config.api_key:
            params = {**params, "apikey": self.config.api_key}

        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"

        for attempt in range(self.config.max_retries + 1):
            try:
                # Rate limiting
                self.rate_limiter.wait_if_needed()
                self.rate_limiter.record_request()

                self.logger.info(
                    f"Making request (attempt {attempt + 1}/"
                    f"{self.config.max_retries + 1}) to {endpoint} - ID: {correlation_id}"
                )

                response = self.session.get(
                    url, params=params, timeout=self.config.timeout_seconds
                )
                response.raise_for_status()

                data = response.json()

                # Service-specific data validation
                validated_data = self._validate_response(data, endpoint)

                # Cache successful result
                self.cache.set(cache_key, validated_data)

                self.logger.info(
                    f"Request successful for {endpoint} - ID: {correlation_id}"
                )
                return validated_data

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    raise RateLimitError(f"Rate limit exceeded: {e}")
                elif response.status_code == 404:
                    raise DataNotFoundError(f"Data not found: {e}")
                elif attempt < self.config.max_retries:
                    wait_time = 2**attempt  # Exponential backoff
                    self.logger.warning(
                        f"HTTP error (attempt {attempt + 1}/"
                        f"{self.config.max_retries + 1}), retrying in {wait_time}s - "
                        f"ID: {correlation_id}, Error: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    raise FinancialServiceError(
                        f"HTTP error after {self.config.max_retries + 1} attempts: {e}"
                    )

            except requests.exceptions.Timeout as e:
                if attempt < self.config.max_retries:
                    wait_time = 2**attempt
                    self.logger.warning(
                        f"Timeout (attempt {attempt + 1}/"
                        f"{self.config.max_retries + 1}), retrying in {wait_time}s - "
                        f"ID: {correlation_id}"
                    )
                    time.sleep(wait_time)
                else:
                    raise APITimeoutError(
                        f"Request timed out after {self.config.max_retries + 1} attempts"
                    )

            except Exception as e:
                if attempt < self.config.max_retries:
                    wait_time = 2**attempt
                    self.logger.warning(
                        f"Request failed (attempt {attempt + 1}/"
                        f"{self.config.max_retries + 1}), retrying in {wait_time}s - "
                        f"ID: {correlation_id}, Error: {e}"
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(
                        f"Request failed after {self.config.max_retries + 1} attempts - "
                        f"ID: {correlation_id}, Error: {e}"
                    )
                    raise FinancialServiceError(f"API request failed: {e}")

    @abstractmethod
    def _validate_response(self, data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
        """
        Validate and transform API response data

        Args:
            data: Raw API response data
            endpoint: API endpoint that was called

        Returns:
            Validated and transformed data

        Raises:
            ValidationError: When response data is invalid
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Service health check for monitoring

        Returns:
            Dictionary containing service health information
        """
        pass

    def cleanup_cache(self) -> None:
        """Clean up expired cache entries"""
        self.cache.cleanup_expired()

    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()

    def get_service_info(self) -> Dict[str, Any]:
        """Get service configuration and status information"""
        return {
            "name": self.config.name,
            "base_url": self.config.base_url,
            "cache_enabled": self.config.cache.enabled,
            "rate_limit_enabled": self.config.rate_limit.enabled,
            "requests_per_minute": self.config.rate_limit.requests_per_minute,
            "cache_ttl_seconds": self.config.cache.ttl_seconds,
            "max_retries": self.config.max_retries,
            "timeout_seconds": self.config.timeout_seconds,
        }
