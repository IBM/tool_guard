from enum import StrEnum
from typing import Any, Dict, List

from pydantic.dataclasses import dataclass


@dataclass
class JobRequisitionSystemStatus(StrEnum):
    """System-defined status for a job requisition in SAP SuccessFactors."""

    APPROVED = "Approved"
    PRE_APPROVED = "Pre-Approved"
    CLOSED = "Closed"


class SuccessFactorsQuestionType(StrEnum):
    """Enumeration of question types in SuccessFactors screening questions."""

    FREE_TEXT = "QUESTION_TEXT"
    NUMERIC = "QUESTION_NUMERIC"
    RATING_SCALES = "QUESTION_RATING"
    MULTIPLE_CHOICE = "QUESTION_MULTI_CHOICE"


class SuccessFactorsRatingScaleFormat(StrEnum):
    """Rating scale types available for screening questions in SuccessFactors."""

    PERFORMANCE_RATING_SCALE = "Performance Rating Scale"
    PIP_RATING_SCALE = "PIP Rating Scale"
    POT = "Pot"
    READINESS = "Readiness"
    DEFAULT_SCALE = "Default Scale"
    INT_SCALE = "IntScale"
    ANNUAL_PERFORMANCE_RATING_SCALE = "Annual Performance Rating Scale"
    LIKERT_SCALE = "Likert"

    def options(self) -> List[str]:
        """Return the list of option labels for this rating scale."""

        return list(self._label_to_score())

    def get_score(self, label: str) -> float:
        """Convert a label to its numeric score."""

        return self._label_to_score().get(label, -1.0)

    def _label_to_score(self) -> Dict[str, Any]:
        """Internal mapping of label to numeric score for each scale."""

        return {
            self.PERFORMANCE_RATING_SCALE: {
                "Unsatisfactory": 1,
                "Needs Development": 2,
                "Meets Expectations": 3,
                "Outstanding": 4,
                "Extraordinary": 5,
            },
            self.PIP_RATING_SCALE: {
                "Unsatisfactory": 1,
                "Satisfactory": 2,
            },
            self.POT: {
                "Low": 1,
                "Medium": 2,
                "High": 3,
            },
            self.READINESS: {
                "3-5 Years": 1,
                "1-2 Years": 2,
                "Ready Now": 3,
            },
            self.DEFAULT_SCALE: {
                "Did Not Meet": 1,
                "Needs Improvement": 2,
                "Met Target": 3,
                "Superior": 4,
            },
            self.INT_SCALE: {
                "Unsatisfactory": 1,
                "Needs Development": 2,
                "Meets Expectations": 3,
                "Outstanding": 4,
                "Extraordinary": 5,
            },
            self.ANNUAL_PERFORMANCE_RATING_SCALE: {
                "Below Expectations": 1,
                "Contributor": 2,
                "Key Contributor": 3,
                "Outstanding Performer": 4,
            },
            self.LIKERT_SCALE: {
                "Strongly Disagree": 1,
                "Disagree": 2,
                "Neutral": 3,
                "Agree": 4,
                "Strongly Agree": 5,
            },
        }.get(self, {})


class Message(StrEnum):
    """Common default messages in SAP SuccessFactors."""

    SEARCH_STATE_MESSAGE = "No states retrieved"
