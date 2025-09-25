import json
import os
from pathlib import Path
from typing import Dict, Optional

import requests
from requests.auth import HTTPBasicAuth

from agent_ready_tools.clients.clients_enums import AccessLevel


class AuthManager:
    """Base Authentication Manager."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
        creds_path: Path,
    ):
        """
        Args:
            token_url: The URL for authentication tokens.
            client_id: The client_id to use for authentication.
            client_secret: The client_secret to use for authentication.
            initial_bearer_token: The initial bearer token.
            initial_refresh_token: The initial refresh token.
            creds_path: The path to the credentials file.
        """
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.initial_bearer_token = initial_bearer_token
        self.initial_refresh_token = initial_refresh_token
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.bearer_token_resp_key = "access_token"
        self.refresh_token_resp_key = "refresh_token"
        self.request_data_template = "grant_type=refresh_token&refresh_token={0}"
        self.creds_path = creds_path
        self.pants_sandbox_substr = "pants-sandbox"

    def _get_cred_from_server_cache(self, key: str) -> Optional[str]:
        """Gets a given key's value from the cached server side."""
        if not self.creds_path.is_file():
            return None
        with open(self.creds_path) as f:
            d: Dict[str, str] = json.load(f)
            return d.get(key)

    def _update_server_creds_cache(self, creds: Dict[str, str]) -> None:
        """Updates the credentials cache."""
        with open(self.creds_path, "w") as f:
            json.dump(creds, f)

    def refresh_bearer_token(self) -> None:
        """Gets and caches a bearer_token using a refresh_token from the auth URL using the loaded
        credentials."""

        if self.pants_sandbox_substr in os.getcwd():
            return
        refresh_token = (
            self._get_cred_from_server_cache(self.refresh_token_resp_key)
            or self.initial_refresh_token
        )

        request_data = self.request_data_template.format(refresh_token)
        response = requests.get(
            url=self.token_url, auth=self.auth, headers=self.headers, data=request_data
        )

        response.raise_for_status()
        resp: Dict[str, Optional[str]] = response.json()
        tokens = {
            key: str(resp[key])
            for key in (self.bearer_token_resp_key, self.refresh_token_resp_key)
            if resp.get(key) is not None
        }
        self._update_server_creds_cache(tokens)

    def get_bearer_token(self) -> str:
        """Fetches bearer token."""
        from_srv = self._get_cred_from_server_cache(self.bearer_token_resp_key)
        return from_srv or self.initial_bearer_token


class GoogleAuthManager(AuthManager):
    """An Authentication Manager for Google."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
    ):
        """
        Args:
            token_url: The URL for authentication tokens.
            client_id: The client_id to use for authentication.
            client_secret: The client_secret to use for authentication.
            initial_bearer_token: The initial bearer token.
            initial_refresh_token: The initial refresh token.
        """
        creds_path = Path(f"/tools/google_auth.json")
        super().__init__(
            token_url,
            client_id,
            client_secret,
            initial_bearer_token,
            initial_refresh_token,
            creds_path,
        )

    def refresh_bearer_token(self) -> None:
        """Gets and caches a bearer_token using a refresh_token from the auth URL using the loaded
        credentials."""
        if self.pants_sandbox_substr in os.getcwd():
            return
        refresh_token = (
            self._get_cred_from_server_cache(self.refresh_token_resp_key)
            or self.initial_refresh_token
        )
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(
            url=self.token_url, auth=self.auth, headers=self.headers, data=payload
        )
        response.raise_for_status()
        resp: Dict[str, Optional[str]] = response.json()
        tokens = {
            self.bearer_token_resp_key: str(resp[self.bearer_token_resp_key]),
            self.refresh_token_resp_key: refresh_token,
        }
        self._update_server_creds_cache(tokens)


class AdobeWorkfrontAuthManager(AuthManager):
    """An Authentication Manager for Adobe Workfront."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
    ):
        """
        Args:
            token_url: The URL for authentication tokens.
            client_id: The client_id to use for authentication.
            client_secret: The client_secret to use for authentication.
            initial_bearer_token: The initial bearer token.
            initial_refresh_token: The initial refresh token.
        """
        creds_path = Path(f"/tools/adobe_workfront_auth.json")
        super().__init__(
            token_url,
            client_id,
            client_secret,
            initial_bearer_token,
            initial_refresh_token,
            creds_path,
        )

    def refresh_bearer_token(self) -> None:
        """Gets and caches a bearer_token using a refresh_token from the auth URL using the loaded
        credentials."""

        if self.pants_sandbox_substr in os.getcwd():
            return
        refresh_token = (
            self._get_cred_from_server_cache(self.refresh_token_resp_key)
            or self.initial_refresh_token
        )
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = requests.post(
            url=self.token_url, auth=self.auth, headers=self.headers, data=payload
        )
        response.raise_for_status()
        resp: Dict[str, Optional[str]] = response.json()
        tokens = {
            key: str(resp[key])
            for key in (self.bearer_token_resp_key, self.refresh_token_resp_key)
            if resp.get(key) is not None
        }
        self._update_server_creds_cache(tokens)


class HubSpotAuthManager(AuthManager):
    """An Authentication Manager for HubSpot."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
    ):
        """
        Args:
            token_url: The URL for authentication tokens.
            client_id: The client_id to use for authentication.
            client_secret: The client_secret to use for authentication.
            initial_bearer_token: The initial bearer token.
            initial_refresh_token: The initial refresh token.
        """
        creds_path = Path(f"/tools/hubspot_auth.json")
        super().__init__(
            token_url,
            client_id,
            client_secret,
            initial_bearer_token,
            initial_refresh_token,
            creds_path,
        )

    def refresh_bearer_token(self) -> None:
        """Gets and caches a bearer_token using a refresh_token from the auth URL using the loaded
        credentials."""
        if self.pants_sandbox_substr in os.getcwd():
            return
        refresh_token = (
            self._get_cred_from_server_cache(self.refresh_token_resp_key)
            or self.initial_refresh_token
        )
        client_id = self._get_cred_from_server_cache(self.client_id) or self.client_id
        client_secret = self._get_cred_from_server_cache(self.client_secret) or self.client_secret
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = requests.post(url=self.token_url, headers=self.headers, data=payload)
        response.raise_for_status()
        resp: Dict[str, Optional[str]] = response.json()
        tokens = {
            self.refresh_token_resp_key: refresh_token,
            self.bearer_token_resp_key: str(resp[self.bearer_token_resp_key]),
        }
        self._update_server_creds_cache(tokens)


class WorkdayAuthManager(AuthManager):
    """An Authentication Manager for Workday."""

    def __init__(
        self,
        token_url: str,
        client_id: str,
        client_secret: str,
        initial_bearer_token: str,
        initial_refresh_token: str,
        access_level: AccessLevel,
    ):
        """
        Args:
            token_url: The URL for authentication tokens.
            client_id: The client_id to use for authentication.
            client_secret: The client_secret to use for authentication.
            initial_bearer_token: The initial bearer token.
            initial_refresh_token: The initial refresh token.
            access_level: The access level (account type) the auth tokens correspond to.
        """
        creds_path = Path(f"/tools/{access_level}_workday_auth.json")
        super().__init__(
            token_url,
            client_id,
            client_secret,
            initial_bearer_token,
            initial_refresh_token,
            creds_path,
        )
