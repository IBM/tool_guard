import json
from typing import Any, Dict, List, Optional, Union

import requests
from requests.exceptions import RequestException

from agent_ready_tools.utils.credentials import CredentialKeys, get_tool_credentials
from agent_ready_tools.utils.systems import Systems

# TODO: Will modify accordingly, this will be default per procurement team.
DEFAULT_SCOPES = [
    "core.accounting.read",
    "core.accounting.write",
    "core.approval.configuration.read",
    "core.approval.configuration.write",
    "core.approval.read",
    "core.approval.write",
    "core.budget.read",
    "core.budget.write",
    "core.business_entity.read",
    "core.business_entity.write",
    "core.catalog.read",
    "core.catalog.write",
    "core.comment.read",
    "core.comment.write",
    "core.common.read",
    "core.common.write",
    "core.contract.read",
    "core.contract.write",
    "core.contracts_template.read",
    "core.contracts_template.write",
    "core.easy_form_response.approval.write",
    "core.easy_form_response.read",
    "core.easy_form_response.write",
    "core.easy_form.read",
    "core.easy_form.write",
    "core.expense.read",
    "core.expense.secure.read",
    "core.expense.secure.write",
    "core.expense.write",
    "core.financial_counterparty.read",
    "core.financial_counterparty.write",
    "core.global_navigation.read",
    "core.integration.read",
    "core.integration.write",
    "core.inventory.adjustment.read",
    "core.inventory.adjustment.write",
    "core.inventory.asn.read",
    "core.inventory.asn.write",
    "core.inventory.balance.read",
    "core.inventory.common.read",
    "core.inventory.common.write",
    "core.inventory.consumption.read",
    "core.inventory.consumption.write",
    "core.inventory.cycle_counts.read",
    "core.inventory.cycle_counts.write",
    "core.inventory.pick_list.read",
    "core.inventory.pick_list.write",
    "core.inventory.receiving.read",
    "core.inventory.receiving.write",
    "core.inventory.return_to_supplier.read",
    "core.inventory.return_to_supplier.write",
    "core.inventory.transaction.read",
    "core.inventory.transfer.read",
    "core.inventory.transfer.write",
    "core.invoice.approval.bypass",
    "core.invoice.approval.write",
    "core.invoice.create",
    "core.invoice.delete",
    "core.invoice.read",
    "core.invoice.write",
    "core.item.read",
    "core.item.write",
    "core.legal_entity.read",
    "core.legal_entity.write",
    "core.notifications_summary.read",
    "core.notifications_summary.write",
    "core.object_translations.read",
    "core.object_translations.write",
    "core.order_header_confirmations.read",
    "core.order_header_confirmations.write",
    "core.order_pad.read",
    "core.order_pad.write",
    "core.pay.charges.read",
    "core.pay.charges.write",
    "core.pay.payment_accounts.read",
    "core.pay.payments.read",
    "core.pay.payments.write",
    "core.pay.statements.read",
    "core.pay.statements.write",
    "core.pay.virtual_cards.read",
    "core.pay.virtual_cards.write",
    "core.payables.allocations.read",
    "core.payables.allocations.write",
    "core.payables.expense.read",
    "core.payables.expense.write",
    "core.payables.external.read",
    "core.payables.external.write",
    "core.payables.invoice.read",
    "core.payables.invoice.write",
    "core.payables.order.read",
    "core.payables.order.write",
    "core.project.read",
    "core.project.write",
    "core.punchout_site.read",
    "core.punchout_site.write",
    "core.purchase_order_change.read",
    "core.purchase_order_change.write",
    "core.purchase_order.read",
    "core.purchase_order.write",
    "core.requisition.read",
    "core.requisition.write",
    "core.revision_record.read",
    "core.sourcing.pending_supplier.read",
    "core.sourcing.pending_supplier.write",
    "core.sourcing.read",
    "core.sourcing.response.award.write",
    "core.sourcing.response.read",
    "core.sourcing.response.write",
    "core.sourcing.write",
    "core.supplier_information_sites.read",
    "core.supplier_information_sites.write",
    "core.supplier_information_tax_registrations.delete",
    "core.supplier_information_tax_registrations.read",
    "core.supplier_information_tax_registrations.write",
    "core.supplier_sharing_settings.read",
    "core.supplier_sharing_settings.write",
    "core.supplier_sites.read",
    "core.supplier_sites.write",
    "core.supplier.read",
    "core.supplier.risk_aware.read",
    "core.supplier.risk_aware.write",
    "core.supplier.write",
    "core.translation.read",
    "core.translation.write",
    "core.uom.read",
    "core.uom.write",
    "core.user_group.read",
    "core.user_group.write",
    "core.user.read",
    "core.user.write",
    "email",
    "login",
    "offline_access",
    "openid",
    "profile",
    "travel_booking.common.read",
    "travel_booking.search.write",
    "travel_booking.team.read",
    "travel_booking.team.write",
    "travel_booking.trip.read",
    "travel_booking.trip.write",
    "travel_booking.user.read",
    "travel_booking.user.write",
    "treasury.cash_management.delete",
    "treasury.cash_management.read",
    "treasury.cash_management.write",
    "treasury.financial_instruments.money_market_fund.write",
    "treasury.financial_instruments.read",
]


class CoupaClient:
    """A remote client for Coupa."""

    def __init__(
        self,
        base_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        scope: Optional[list[str]] = None,
    ):
        """
        Args:
            base_url: The base URL for the Coupa API.
            token_url: The URL for authentication tokens for the Coupa API.
            client_id: The client id to authenticate with.
            client_secret: The client id to authenticate with.
            scope: A list of scopes which is used to get token for API requests in Coupa.
        """
        self.base_url = base_url
        self.token_url = token_url
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.client_id = client_id
        self.client_secret = client_secret
        self.bearer = self.get_coupa_oauth_token(scope=DEFAULT_SCOPES if scope is None else scope)
        assert self.bearer

    # TODO: modularize in followup PR so there's less repetition of the try except block
    def delete_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> Union[int, Dict[str, Any]]:
        """
        Executes a DELETE request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            HTTP status code on success, or an error dictionary on failure.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.delete(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                json=payload,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.status_code
        except RequestException:
            if response is not None:
                response_json = {
                    "errors": {
                        "error_message": "Delete request failed",
                        "status_code": getattr(response, "status_code", "Unknown"),
                    }
                }
            else:
                # connection error, timeout, etc.
                response_json = {
                    "errors": {
                        "error_message": "No response received (request failed before getting a response)",
                    }
                }

            return response_json

    def patch_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a PATCH request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.patch(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                json=payload,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = {
                        "errors": {
                            "error_message": "Non-JSON response",
                            "status_code": getattr(response, "status_code", "Unknown"),
                        }
                    }
            else:
                # connection error, timeout, etc.
                response_json = {
                    "errors": {
                        "error_message": "No response received (request failed before getting a response)",
                    }
                }

            return response_json

    def put_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a PUT request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.put(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                json=payload,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = {
                        "errors": {
                            "error_message": "Non-JSON response",
                            "status_code": getattr(response, "status_code", "Unknown"),
                        }
                    }
            else:
                # connection error, timeout, etc.
                response_json = {
                    "errors": {
                        "error_message": "No response received (request failed before getting a response)",
                    }
                }

            return response_json

    def post_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a POST request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.post(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                json=payload,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = {
                        "errors": {
                            "error_message": "Non-JSON response",
                            "status_code": getattr(response, "status_code", "Unknown"),
                        }
                    }
            else:
                # connection error, timeout, etc.
                response_json = {
                    "errors": {
                        "error_message": "No response received (request failed before getting a response)",
                    }
                }

            return response_json

    def post_request_list(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
        payload: Optional[dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes a POST request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.
            payload: The request payload.

        Returns:
            The JSON response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.post(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                json=payload,
                params=json.dumps(params),
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = [{"errors": "Non-JSON response"}]
            else:
                # connection error, timeout, etc.
                response_json = [
                    {
                        "errors": {
                            "error_message": "No response received (request failed before getting a response)",
                        }
                    }
                ]

            if isinstance(response_json, list):
                return response_json
            else:
                return [response_json]

    def get_request(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes a GET request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.get(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = {
                        "errors": {
                            "error_message": "Non-JSON response",
                            "status_code": getattr(response, "status_code", "Unknown"),
                        }
                    }
            else:
                # connection error, timeout, etc.
                response_json = {
                    "errors": {
                        "error_message": "No response received (request failed before getting a response)",
                    }
                }

            return response_json

    def get_request_list(
        self,
        resource_name: str,
        params: Optional[dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes a GET request against Coupa API.

        Args:
            resource_name: The specific resource to make the request against.
            params: Query parameters for the REST API.

        Returns:
            The JSON list response from the Coupa REST API.
        """
        headers = {
            "Authorization": f"Bearer {self.bearer}",
            "Accept": self.headers["Accept"],
        }

        response = None
        try:
            response = requests.get(
                url=f"{self.base_url}/api/{resource_name}",
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except RequestException:
            if response is not None:
                try:
                    response_json = response.json()
                except ValueError:
                    # handle the case where response content is not JSON (e.g. 404)
                    response_json = [{"errors": "Non-JSON response"}]
            else:
                # connection error, timeout, etc.
                response_json = [
                    {
                        "errors": {
                            "error_message": "No response received (request failed before getting a response)",
                        }
                    }
                ]

            if isinstance(response_json, list):
                return response_json
            else:
                return [response_json]

    def get_coupa_oauth_token(self, scope: list[str]) -> str:
        """
        Args:
            scope: A list of scopes which is used to get token for API requests in Coupa.

        Returns:
            An access token for the specific scope(s).
        """
        # Prepare the request payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(scope),
        }

        # Make the POST request to obtain the token
        try:
            response = requests.post(self.token_url, headers=self.headers, data=payload)
        except RequestException:
            return ""

        access_token = ""

        # Check if the request was successful
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]

        return access_token


def get_coupa_client(scope: Optional[list[str]] = None) -> CoupaClient:
    """
    Get the coupa client with credentials.

    NOTE: DO NOT CALL DIRECTLY IN TESTING!

    To test, either mock this call or call the client directly.

    Args:
        scope: A list of scopes which is used to get token for API requests in Coupa.

    Returns:
        A new instance of CoupaClient.
    """
    credentials = get_tool_credentials(Systems.COUPA)
    coupa_client = CoupaClient(
        base_url=credentials[CredentialKeys.BASE_URL],
        token_url=credentials[CredentialKeys.TOKEN_URL],
        client_id=credentials[CredentialKeys.CLIENT_ID],
        client_secret=credentials[CredentialKeys.CLIENT_SECRET],
        scope=scope,
    )
    return coupa_client
