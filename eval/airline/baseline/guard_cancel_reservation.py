from typing import *

import airline
from rt_toolguard.data_types import PolicyViolationException
from airline.airline_types import *
from airline.i_airline import I_Airline

from airline.cancel_reservation.guard_obtain_required_information_before_cancellation import guard_obtain_required_information_before_cancellation
from airline.cancel_reservation.guard_allow_cancellation_within_24_hours_of_booking import guard_allow_cancellation_within_24_hours_of_booking
from airline.cancel_reservation.guard_allow_cancellation_if_airline_cancelled_the_flight import guard_allow_cancellation_if_airline_cancelled_the_flight
from airline.cancel_reservation.guard_basic_economy_or_economy_cancellation_rules_without_24h_or_airline_cancellation_conditions import guard_basic_economy_or_economy_cancellation_rules_without_24h_or_airline_cancellation_conditions
from airline.cancel_reservation.guard_business_class_cancellation_rules_without_24h_or_airline_cancellation_conditions import guard_business_class_cancellation_rules_without_24h_or_airline_cancellation_conditions
from airline.cancel_reservation.guard_only_cancel_trips_that_are_not_flown import guard_only_cancel_trips_that_are_not_flown
from airline.cancel_reservation.guard_obtain_explicit_user_confirmation_before_cancellation import guard_obtain_explicit_user_confirmation_before_cancellation


def guard_cancel_reservation(api: I_Airline, reservation_id: str):
    """
    Checks that a tool call complies to the policies.

    Args:
        api (I_Airline): api to access other tools.
        reservation_id: The reservation ID, such as 'ZFA04Y'.
         

    Raises:
        PolicyViolationException: If the tool call does not comply to the policy.
    """
    
    pass #FIXME
