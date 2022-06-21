import json
import responses
import pytest
import re

import pyoncat

########################################################################
# Fixtures / Constants
########################################################################


class MockONCatServer(object):
    def __init__(self, oauth_provider):
        self.oauth_provider = oauth_provider

        self.calls = []
        self._response_status = None
        self._response_headers = None
        self._response_body = None

    def set_response(self, status=None, headers=None, body=None):
        self._response_status = status if status else 200
        self._response_headers = headers if headers else {}
        self._response_body = json.dumps(body) if body else ""

    def __call__(self, request):
        assert (
            request.headers["Authorization"]
            == "Bearer %s" % self.oauth_provider.most_recent_access_token
        )

        self.calls.append(request)

        return (
            self._response_status,
            self._response_headers,
            self._response_body,
        )


@pytest.yield_fixture
def oncat_client_and_mock_oncat_server():
    oauth_provider = pytest.helpers.MockOAuthProvider()
    oncat_server = MockONCatServer(oauth_provider)

    with responses.RequestsMock(assert_all_requests_are_fired=False) as r:
        r.add_callback(
            responses.POST,
            "https://oncat.ornl.gov/oauth/token",
            callback=oauth_provider,
            content_type="application/json;charset=utf-8",
            match_querystring=True,
        )
        for method in [
            responses.GET,
            responses.PUT,
            responses.POST,
            responses.DELETE,
        ]:
            r.add_callback(
                method,
                # Match everything but the /oauth/token URL
                re.compile(r"https://oncat\.ornl\.gov(?!/oauth/token).*"),
                callback=oncat_server,
                content_type="application/json;charset=utf-8",
                match_querystring=True,
            )

        scopes = ["api:read"]
        client_id, client_secret = oauth_provider.register_client(scopes)

        oncat_client = pyoncat.ONCat(
            "https://oncat.ornl.gov",
            client_id=client_id,
            client_secret=client_secret,
            flow=pyoncat.CLIENT_CREDENTIALS_FLOW,
            scopes=scopes,
        )

        yield oncat_client, oncat_server


########################################################################
# Tests
########################################################################


def test_get(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    # Test retrieval of a single item.
    resource = {"name": "A", "id": "A", "object": "resource"}
    oncat_server.set_response(200, body=resource)
    assert oncat_client.get("/api/resources/A") == resource
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/api/resources/A"
    assert oncat_server.calls[-1].body is None

    # Test retrieval of single item which does not exist.  Note that
    # this also covers the case where an item *does* exist and we're
    # just not authorized to see it -- the API returns a 404 to prevent
    # leaking information.
    oncat_server.set_response(
        404, body={"message": "Resource does not exist."}
    )
    with pytest.raises(pyoncat.NotFoundError):
        oncat_client.get("/api/resources/A")
    assert len(oncat_server.calls) == 2
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/api/resources/A"
    assert oncat_server.calls[-1].body is None

    # Test retrieval of an item for which we do not have the required
    # scope.
    oncat_server.set_response(
        401, body={"message": "Required scope is missing: admin:read."}
    )
    with pytest.raises(pyoncat.UnauthorizedError):
        oncat_client.get("/admin/resources/A")
    assert len(oncat_server.calls) == 3
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/admin/resources/A"
    assert oncat_server.calls[-1].body is None

    # Test retrieval of multiple items.
    resources = [
        {"name": "A", "id": "A", "object": "resource"},
        {"name": "B", "id": "B", "object": "resource"},
    ]
    oncat_server.set_response(200, body=resources)
    assert oncat_client.get("/api/resources") == resources
    assert len(oncat_server.calls) == 4
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/api/resources"
    assert oncat_server.calls[-1].body is None

    # Test retrieval of single item but where an error was thrown that
    # we were not expecting, and for which we don't throw a particular
    # PyONCatError.
    oncat_server.set_response(400, body={"message": "Bad request."})
    with pytest.raises(pyoncat.PyONCatError):
        oncat_client.get("/api/resources/A")
    assert len(oncat_server.calls) == 5
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/api/resources/A"
    assert oncat_server.calls[-1].body is None


def test_put(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    # Test the creation of a single item via PUT.
    resource = {"name": "A", "id": "A", "object": "resource"}
    oncat_server.set_response(200, body=resource)
    assert oncat_client.put("/api/resources/A", resource) == resource
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "PUT"
    assert oncat_server.calls[-1].path_url == "/api/resources/A"
    assert json.loads(oncat_server.calls[-1].body) == resource


def test_post(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    # Test the creation of a single item via POST.
    resource = {"name": "A", "id": "A", "object": "resource"}
    oncat_server.set_response(201, body=resource)
    assert oncat_client.post("/api/resources", resource) == resource
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "POST"
    assert oncat_server.calls[-1].path_url == "/api/resources"
    assert json.loads(oncat_server.calls[-1].body) == resource


def test_delete(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    # Test the deletion of a single item.
    oncat_server.set_response(204)
    assert oncat_client.delete("/api/resources/A") is None
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "DELETE"
    assert oncat_server.calls[-1].path_url == "/api/resources/A"
    assert oncat_server.calls[-1].body is None


########################################################################


def test_resource_retrieve(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    instrument = {"name": "NOM", "id": "NOM", "object": "instrument"}
    oncat_server.set_response(200, body=instrument)
    assert (
        oncat_client.Instrument.retrieve("NOM", facility="SNS").to_dict()
        == instrument
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "GET"
    assert (
        oncat_server.calls[-1].path_url == "/api/instruments/NOM?facility=SNS"
    )
    assert oncat_server.calls[-1].body is None


def test_resource_list(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    instruments = [
        {"name": "CNCS", "id": "CNCS", "object": "instrument"},
        {"name": "NOM", "id": "NOM", "object": "instrument"},
    ]
    oncat_server.set_response(200, body=instruments)
    assert [
        instrument.to_dict()
        for instrument in oncat_client.Instrument.list(facility="SNS")
    ] == instruments
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "GET"
    assert oncat_server.calls[-1].path_url == "/api/instruments?facility=SNS"
    assert oncat_server.calls[-1].body is None


def test_resource_place(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    cache_entry = {"key": "ldap/pp4", "value": ["IPTS-1234"]}
    oncat_server.set_response(200, body=cache_entry)
    assert (
        oncat_client.CacheEntry.place(
            "ldap/pp4", cache_entry, param="value"
        ).to_dict()
        == cache_entry
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "PUT"
    assert (
        oncat_server.calls[-1].path_url == "/admin/cache/ldap/pp4?param=value"
    )
    assert json.loads(oncat_server.calls[-1].body) == cache_entry


def test_resource_create(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    template = {"instrument": "NOM", "columns": []}
    oncat_server.set_response(200, body=template)
    assert (
        oncat_client.Template.create(template, instrument="NOM").to_dict()
        == template
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "POST"
    assert (
        oncat_server.calls[-1].path_url == "/settings/templates?instrument=NOM"
    )
    assert json.loads(oncat_server.calls[-1].body) == template


def test_resource_remove(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    oncat_server.set_response(204)
    assert oncat_client.Template.remove("template-id") is None
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "DELETE"
    assert oncat_server.calls[-1].path_url == "/settings/templates/template-id"
    assert oncat_server.calls[-1].body is None


########################################################################


def test_sub_resource_retrieve(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    experiment_archive = {"id": "IPTS-1234", "data_available": True}
    oncat_server.set_response(200, body=experiment_archive)
    assert (
        oncat_client.ExperimentArchive.retrieve(
            "IPTS-1234", instrument="NOM"
        ).to_dict()
        == experiment_archive
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "GET"
    assert (
        oncat_server.calls[-1].path_url
        == "/api/experiments/IPTS-1234/archive?instrument=NOM"
    )
    assert oncat_server.calls[-1].body is None


def test_sub_resource_place(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    experiment_archive = {"id": "IPTS-1234", "data_available": True}
    oncat_server.set_response(200, body=experiment_archive)
    assert (
        oncat_client.ExperimentArchive.place(
            "IPTS-1234", experiment_archive, instrument="NOM"
        ).to_dict()
        == experiment_archive
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "PUT"
    assert (
        oncat_server.calls[-1].path_url
        == "/api/experiments/IPTS-1234/archive?instrument=NOM"
    )
    assert json.loads(oncat_server.calls[-1].body) == experiment_archive


def test_sub_resource_create(oncat_client_and_mock_oncat_server):
    oncat_client, oncat_server = oncat_client_and_mock_oncat_server

    datafile_location = {"location": "/FAC/INST/IPTS-1234/1.nxs"}
    datafile = {"location": "/FAC/INST/IPTS-1234/1.nxs", "metadata": {}}
    oncat_server.set_response(201, body=datafile)
    assert (
        oncat_client.DatafileLocation.create(
            datafile_location, param="value"
        ).to_dict()
        == datafile
    )
    assert len(oncat_server.calls) == 1
    assert oncat_server.calls[-1].method == "POST"
    assert (
        oncat_server.calls[-1].path_url
        == "/api/datafiles/location?param=value"
    )
    assert json.loads(oncat_server.calls[-1].body) == datafile_location


########################################################################


def test_resource_meta(oncat_client_and_mock_oncat_server):
    oncat_client, _ = oncat_client_and_mock_oncat_server

    # Make sure we throw a standard error when calling a resource which
    # does not exist.
    with pytest.raises(AttributeError) as exc:
        oncat_client.ResourceDoesNotExist.list()
    assert "'ONCat' object has no attribute 'ResourceDoesNotExist'" in str(exc)

    # Make sure resources are listed correctly in calls to dir().
    assert "Datafile" in dir(oncat_client)


########################################################################


def test_representation():
    dummy_content = {
        "object": "dummy",
        "id": "6454f70d-9ab8-48cc-a3d9-f44ca261c29b",
        "nested": {
            "deeply": {"a": 1, "b": 2, "c": 3},
            "field": 1234.567,
            "field@units": "m",
        },
        "a_string": "abcdef",
        "array": [{"key": "value_a"}, {"key": "value_b"}, {"key": "value_c"}],
    }
    dummy = pyoncat.ONCatRepresentation(content=dummy_content)

    assert dummy.to_dict() == dummy_content

    # Test str and repr printouts.
    assert '"id": "6454f70d-9ab8-48cc-a3d9-f44ca261c29b",' in str(dummy)
    assert '"id": "6454f70d-9ab8-48cc-a3d9-f44ca261c29b",' in repr(dummy)
    assert "id=6454f70d-9ab8-48cc-a3d9-f44ca261c29b" in repr(dummy)
    assert "object=dummy" in repr(dummy)

    # Old syntax.
    assert dummy.nested["deeply"]["a"] == 1
    # New syntax.
    assert dummy["nested.deeply.a"] == 1

    # Old way to deal with missing values.
    with pytest.raises(KeyError):
        dummy["nested.deeply.d"]
    with pytest.raises(KeyError):
        dummy["does.not.exist"]
    with pytest.raises(KeyError):
        dummy["array.key"]

    # New way to deal with missing values.
    assert dummy.get("nested.deeply.d") is None
    assert dummy.get("nested.deeply.d", default=1) == 1
    assert dummy.get("array.key", default=1) == 1

    assert sorted(dummy.nodes()) == [
        "a_string",
        "array",
        "id",
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
        "nested.field",
        "nested.field@units",
        "object",
    ]
    assert sorted(dummy.nodes(root="nested")) == [
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
        "nested.field",
        "nested.field@units",
    ]
    assert sorted(dummy.nodes(root="nested.deeply")) == [
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
    ]

    assert sorted(dummy.nodes(include_branches=True)) == [
        "a_string",
        "array",
        "id",
        "nested",
        "nested.deeply",
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
        "nested.field",
        "nested.field@units",
        "object",
    ]
    assert sorted(dummy.nodes(root="nested", include_branches=True)) == [
        "nested",
        "nested.deeply",
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
        "nested.field",
        "nested.field@units",
    ]
    assert sorted(
        dummy.nodes(root="nested.deeply", include_branches=True)
    ) == [
        "nested.deeply",
        "nested.deeply.a",
        "nested.deeply.b",
        "nested.deeply.c",
    ]
