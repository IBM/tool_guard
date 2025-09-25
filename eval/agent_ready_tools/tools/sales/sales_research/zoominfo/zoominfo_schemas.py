from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class ErrorResponse:
    """Represent the Error Response in Zoominfo API."""

    message: Any
    status_code: Any


@dataclass
class ZoominfoContact:
    """Dataclass representing on search contact response from Zoominfo."""

    person_id: int  # mapped from id
    first_name: str  # mapped from firstName
    last_name: str  # mapped from lastName
    job_title: str  # mapped from jobTitle
    company_name: str  # mapped from companyName
    has_email: bool  # mapped from hasEmail


@dataclass
class ZoominfoEnrichedContact:
    """Dataclass representing on enriched contacts from Zoominfo."""

    first_name: str  # mapped from firstName
    last_name: str  # mapped from lastName
    email: str  # mapped from email
    city: str  # mapped from city
    job_title: str  # mapped from jobTitle
    job_function: str  # mapped from jobFunction
    company_name: str  # mapped from companyName
    social_media: str  # mapped from externalUrls
