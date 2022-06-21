import json
import pytest
import random
import string
import uuid


@pytest.helpers.register
class MockOAuthProvider(object):
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.username = None
        self.password = None
        self.scopes = None
        self.most_recent_access_token = None
        self.most_recent_refresh_token = None
        self.client_credentials_call_count = 0
        self.password_call_count = 0
        self.refresh_token_call_count = 0

        self.default_expiration = 7199

    def _generate_access_token(self):
        self.most_recent_access_token = _generate_token()
        return self.most_recent_access_token

    def _generate_refresh_token(self):
        self.most_recent_refresh_token = _generate_token()
        return self.most_recent_refresh_token

    def register_client(self, scopes):
        self.scopes = scopes
        self.client_id, self.client_secret = (
            str(uuid.uuid4()),
            str(uuid.uuid4()),
        )

        return self.client_id, self.client_secret

    def register_user(self):
        self.username, self.password = (str(uuid.uuid4()), str(uuid.uuid4()))

        return self.username, self.password

    def __call__(self, request):
        assert request.method == "POST"
        assert (
            request.headers["Content-Type"]
            == "application/x-www-form-urlencoded;charset=UTF-8"
        )

        response_headers = {"Content-Type": "application/json;charset=utf-8"}

        if "grant_type=client_credentials" in request.body:
            self.client_credentials_call_count += 1

            if (
                not "client_id=%s" % self.client_id in request.body
                or not "client_secret=%s" % self.client_secret in request.body
            ):
                return (
                    400,
                    response_headers,
                    json.dumps(
                        {
                            "error": "invalid_client",
                            "error_description": "Invalid client or client "
                            "credentials",
                        }
                    ),
                )

            for scope in self.scopes:
                assert scope.replace(":", "%3A") in request.body

            response_body = {
                "access_token": self._generate_access_token(),
                "token_type": "Bearer",
                "expires_in": self.default_expiration,
            }

            return (200, response_headers, json.dumps(response_body))

        if "grant_type=password" in request.body:
            self.password_call_count += 1

            if (
                not "client_id=%s" % self.client_id in request.body
                or not "client_secret=%s" % self.client_secret in request.body
            ):
                return (
                    400,
                    response_headers,
                    json.dumps(
                        {
                            "error": "invalid_client",
                            "error_description": "Invalid client or client "
                            "credentials",
                        }
                    ),
                )

            if (
                not "username=%s" % self.username in request.body
                or not "password=%s" % self.password in request.body
            ):
                return (
                    400,
                    response_headers,
                    json.dumps(
                        {
                            "error": "invalid_grant",
                            "error_description": "System error: fail to "
                            "process username & password combination.",
                        }
                    ),
                )

            for scope in self.scopes:
                assert scope.replace(":", "%3A") in request.body

            response_body = {
                "access_token": self._generate_access_token(),
                "refresh_token": self._generate_refresh_token(),
                "token_type": "Bearer",
                "expires_in": self.default_expiration,
            }
            return (200, response_headers, json.dumps(response_body))

        if "grant_type=refresh_token" in request.body:
            self.refresh_token_call_count += 1

            assert "client_id=%s" % self.client_id in request.body
            # Clients that have been given a secret need to use it to
            # refresh tokens.
            if self.client_secret:
                assert "client_secret=%s" % self.client_secret in request.body
            if (
                not "refresh_token=%s" % self.most_recent_refresh_token
                in request.body
            ):
                return (
                    400,
                    response_headers,
                    json.dumps(
                        {
                            "error": "invalid_grant",
                            "error_description": "unknown, invalid, or "
                            "expired refresh token",
                        }
                    ),
                )
            assert "refresh_token=%s" % self.most_recent_refresh_token
            for scope in self.scopes:
                assert scope.replace(":", "%3A") in request.body

            response_body = {
                "access_token": self._generate_access_token(),
                "refresh_token": self._generate_refresh_token(),
                "token_type": "Bearer",
                "expires_in": self.default_expiration,
            }
            return (200, response_headers, json.dumps(response_body))

        assert False


########################################################################
# Helpers
########################################################################


def _generate_token():
    # From: https://stackoverflow.com/a/2257449/778572
    return "".join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(32)
    )
