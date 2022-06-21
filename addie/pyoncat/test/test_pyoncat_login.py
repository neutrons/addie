import datetime
import responses
import pytest
import re

import pyoncat

########################################################################
# Fixtures / Constants
########################################################################

TEST_START_TIME = datetime.datetime.now()


class MockAuthCheckerONCatServer(object):
    def __init__(self, oauth_provider):
        self.oauth_provider = oauth_provider

    def __call__(self, request):
        assert (
            request.headers["Authorization"]
            == "Bearer %s" % self.oauth_provider.most_recent_access_token
        )

        return (200, {}, "")


@pytest.yield_fixture
def mock_oauth_provider():
    oauth_provider = pytest.helpers.MockOAuthProvider()
    oncat_server = MockAuthCheckerONCatServer(oauth_provider)

    with responses.RequestsMock(assert_all_requests_are_fired=False) as r:
        r.add_callback(
            responses.POST,
            "https://oncat.ornl.gov/oauth/token",
            callback=oauth_provider,
            content_type="application/json;charset=utf-8",
            match_querystring=True,
        )
        r.add_callback(
            responses.GET,
            # Match everything but the /oauth/token URL
            re.compile(r"https://oncat\.ornl\.gov(?!/oauth/token).*"),
            callback=oncat_server,
            content_type="application/json;charset=utf-8",
            match_querystring=True,
        )

        yield oauth_provider


########################################################################
# Tests
########################################################################


@pytest.mark.freeze_time(TEST_START_TIME)
def test_invalid_client_credentials(mock_oauth_provider):
    scopes = ["api:read", "admin:read"]

    client_id, client_secret = mock_oauth_provider.register_client(scopes)

    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id="INCORRECT_CLIENT_ID",
        client_secret=client_secret,
        flow=pyoncat.CLIENT_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    with pytest.raises(pyoncat.InvalidClientCredentialsError):
        oncat.login()


@pytest.mark.freeze_time(TEST_START_TIME)
def test_client_credentials_used_after_login(freezer, mock_oauth_provider):
    scopes = ["api:read", "admin:read"]

    client_id, client_secret = mock_oauth_provider.register_client(scopes)

    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        flow=pyoncat.CLIENT_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    # Implicit login should trigger a token request.
    oncat.get("/api/facilities")
    assert mock_oauth_provider.client_credentials_call_count == 1

    # Subsequent calls should not trigger a further request.
    oncat.get("/api/facilities")
    assert mock_oauth_provider.client_credentials_call_count == 1

    # But an explicit call to login should trigger another request.
    oncat.login()
    assert mock_oauth_provider.client_credentials_call_count == 2
    oncat.get("/api/facilities")
    assert mock_oauth_provider.client_credentials_call_count == 2

    # The token should work right up until the expiration.
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(
            seconds=mock_oauth_provider.default_expiration - 1
        )
    )
    oncat.get("/api/facilities")
    assert mock_oauth_provider.client_credentials_call_count == 2

    # But a new token should be retrieved as soon as it has expired.
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
    )
    oncat.get("/api/facilities")
    assert mock_oauth_provider.client_credentials_call_count == 3


@pytest.mark.freeze_time(TEST_START_TIME)
def test_invalid_resource_owner_credentials(freezer, mock_oauth_provider):
    scopes = ["api:read", "admin:read"]

    client_id, client_secret = mock_oauth_provider.register_client(scopes)
    username, password = mock_oauth_provider.register_user()

    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id="INCORRECT_CLIENT_ID",
        client_secret=client_secret,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    with pytest.raises(pyoncat.InvalidClientCredentialsError):
        oncat.login(username, password)

    # Now log in correctly, and force a refresh with an invalid refresh
    # token.
    token_store = pyoncat.InMemoryTokenStore()
    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        token_getter=token_store.get_token,
        token_setter=token_store.set_token,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )
    oncat.login(username, password)
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
    )
    token = token_store.get_token()
    token["refresh_token"] = "INVALID_REFRESH_TOKEN"
    token_store.set_token(token)
    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        token_getter=token_store.get_token,
        token_setter=token_store.set_token,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )
    with pytest.raises(pyoncat.InvalidRefreshTokenError):
        oncat.get("api/facilities")


@pytest.mark.freeze_time(TEST_START_TIME)
def test_resource_owner_credentials_used_after_login(
    freezer, mock_oauth_provider
):
    scopes = ["api:read", "admin:read"]

    client_id, client_secret = mock_oauth_provider.register_client(scopes)
    username, password = mock_oauth_provider.register_user()

    oncat = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    # Implicit logins don't work with this flow without an existing
    # token.
    with pytest.raises(pyoncat.LoginRequiredError):
        oncat.get("/api/facilities")

    # Providing a username and password is mandatory when logging in.
    with pytest.raises(pyoncat.LoginRequiredError):
        oncat.login()

    oncat.login(username, password)
    assert mock_oauth_provider.password_call_count == 1
    oncat.get("/api/facilities")
    assert mock_oauth_provider.password_call_count == 1

    # The token should work right up until the expiration.
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(
            seconds=mock_oauth_provider.default_expiration - 1
        )
    )
    oncat.get("/api/facilities")
    assert mock_oauth_provider.password_call_count == 1

    # But a refresh should be triggered as soon as it has expired.
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
    )
    oncat.get("/api/facilities")
    assert mock_oauth_provider.refresh_token_call_count == 1
    assert mock_oauth_provider.password_call_count == 1

    # And a further refresh triggered as soon as that one has expired.
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
    )
    oncat.get("/api/facilities")
    assert mock_oauth_provider.refresh_token_call_count == 2
    assert mock_oauth_provider.password_call_count == 1

    # Make sure a further (unnecessary) login doesn't hurt anything.
    oncat.login(username, password)
    assert mock_oauth_provider.password_call_count == 2
    oncat.get("/api/facilities")
    assert mock_oauth_provider.password_call_count == 2
    assert mock_oauth_provider.refresh_token_call_count == 2


@pytest.mark.freeze_time(TEST_START_TIME)
def test_resource_owner_credentials_token_persistence(
    freezer, mock_oauth_provider
):
    scopes = ["api:read", "admin:read"]

    client_id, client_secret = mock_oauth_provider.register_client(scopes)
    username, password = mock_oauth_provider.register_user()

    token_store = pyoncat.InMemoryTokenStore()

    first_oncat_instance = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        token_getter=token_store.get_token,
        token_setter=token_store.set_token,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    first_oncat_instance.login(username, password)
    assert mock_oauth_provider.password_call_count == 1

    # We're not trying to test for asynchronicity or anything like that.
    # To make it clear, let's get rid of the old instance entirely.
    del first_oncat_instance

    # Pretend a second instance of PyONCat has been started, with access
    # to the original's tokens.
    second_oncat_instance = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        token_getter=token_store.get_token,
        token_setter=token_store.set_token,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    # We should be able to pick up where we left off.
    second_oncat_instance.get("/api/facilities")
    assert mock_oauth_provider.password_call_count == 1

    # And a third instance should be able to do likewise, even if a
    # refresh is needed.
    del second_oncat_instance
    freezer.move_to(
        TEST_START_TIME
        + datetime.timedelta(seconds=mock_oauth_provider.default_expiration)
    )
    third_oncat_instance = pyoncat.ONCat(
        "https://oncat.ornl.gov",
        client_id=client_id,
        client_secret=client_secret,
        token_getter=token_store.get_token,
        token_setter=token_store.set_token,
        flow=pyoncat.RESOURCE_OWNER_CREDENTIALS_FLOW,
        scopes=scopes,
    )

    third_oncat_instance.get("/api/facilities")
    assert mock_oauth_provider.password_call_count == 1
    assert mock_oauth_provider.refresh_token_call_count == 1
