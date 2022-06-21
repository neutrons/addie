import json
import requests
import os
import sys
import weakref

from .lib import six

import oauthlib.oauth2
import requests_oauthlib

from requests.packages.urllib3.exceptions import InsecureRequestWarning

import warnings

########################################################################
# Exceptions
########################################################################


class PyONCatError(Exception):
    def __init__(self, message=None, original_error=None):
        if not message:
            message = ""
        try:
            message += " [" + original_error.response.json()["message"] + "]"
        except Exception:
            pass
        super(PyONCatError, self).__init__(message)
        self.original_error = original_error


class UnauthorizedError(PyONCatError):
    pass


class InvalidClientCredentialsError(PyONCatError):
    pass


class InvalidUserCredentialsError(PyONCatError):
    pass


class InvalidRefreshTokenError(PyONCatError):
    pass


class LoginRequiredError(PyONCatError):
    pass


class NotFoundError(PyONCatError):
    pass


def pyoncat_raise(error):
    six.raise_from(error, None)


########################################################################
# Resources / Representations
########################################################################


class _ONCatResourceMeta(type):
    REGISTERED_RESOURCES = []

    def __init__(cls, *args):
        super(_ONCatResourceMeta, cls).__init__(args)
        if not cls.__name__.startswith("_"):
            _ONCatResourceMeta.REGISTERED_RESOURCES.append(cls)


class ONCatRepresentation(object):
    def __init__(self, content):
        self._content = content

    def __repr__(self):
        # https://stackoverflow.com/a/2626364/778572
        ident_parts = [type(self).__name__]

        ident_parts.append("object=%s" % (
            self._content.get("object") or self._content.get("type")
        ))
        ident_parts.append("id=%s" % (self._content.get("id")))

        unicode_repr = "<%s at %s> JSON: %s" % (
            " ".join(ident_parts),
            hex(id(self)),
            str(self),
        )

        if sys.version_info[0] < 3:
            return unicode_repr.encode("utf-8")
        else:
            return unicode_repr

    def __str__(self):
        return json.dumps(self._content, sort_keys=True, indent=4)

    def __getattr__(self, k):
        if k[0] == "_":
            raise AttributeError(k)

        try:
            return self._content[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __getitem__(self, key):
        elements = key.split(".")
        if len(elements) > 1:
            current = elements[0]
            remainder = elements[1:]
        else:
            current = elements[0]
            remainder = None

        if isinstance(self._content[current], dict):
            value = ONCatRepresentation(content=self._content[current])

            if remainder:
                remainder = ".".join(remainder)
                return value.__getitem__(remainder)
        else:
            if remainder:
                raise KeyError(".".join(remainder))
            value = self._content[current]

        return value

    def to_dict(self):
        return self._content

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def nodes(self, root=None, include_branches=False):
        result = sorted(_yield_nodes(self._content, None, include_branches))

        if root:
            # TODO: Not the most performant way of doing this...
            return [key for key in result if key.startswith(root)]
        return result


@six.add_metaclass(_ONCatResourceMeta)
class _ONCatResource(object):
    def __init__(self, parent_oncat):
        self._parent_oncat_weakref = weakref.ref(parent_oncat)

    def retrieve(self, identifier, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            identifier,
        )

        return ONCatRepresentation(content=oncat.get(path, **kwargs))


@six.add_metaclass(_ONCatResourceMeta)
class _ONCatSubResource(object):
    def __init__(self, parent_oncat):
        self._parent_oncat_weakref = weakref.ref(parent_oncat)

    def retrieve(self, identifier, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            identifier,
            self._SUB_RESOURCE_ENDPOINT,
        )

        return ONCatRepresentation(content=oncat.get(path, **kwargs))


class _ListableONCatResource(_ONCatResource):
    def list(self, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s" % (self._NAMESPACE, self._RESOURCE_ENDPOINT)

        return [
            ONCatRepresentation(content=content)
            for content in oncat.get(path, **kwargs)
        ]


class _UpdatableONCatResource(_ONCatResource):
    def place(self, identifier, data, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            identifier,
        )

        return ONCatRepresentation(content=oncat.put(path, data, **kwargs))


class _UpdatableONCatSubResource(_ONCatSubResource):
    def place(self, identifier, data, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            identifier,
            self._SUB_RESOURCE_ENDPOINT,
        )

        return ONCatRepresentation(content=oncat.put(path, data, **kwargs))


class _CreatableONCatResource(_ONCatResource):
    def create(self, data, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s" % (self._NAMESPACE, self._RESOURCE_ENDPOINT)

        return ONCatRepresentation(content=oncat.post(path, data, **kwargs))


class _CreatableONCatSubResource(_ONCatSubResource):
    def create(self, data, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            self._SUB_RESOURCE_ENDPOINT,
        )

        return ONCatRepresentation(content=oncat.post(path, data, **kwargs))


class _RemovableONCatResource(_ONCatResource):
    def remove(self, identifier, **kwargs):
        oncat = self._parent_oncat_weakref()

        path = "%s/%s/%s" % (
            self._NAMESPACE,
            self._RESOURCE_ENDPOINT,
            identifier,
        )

        oncat.delete(path, **kwargs)


########################################################################


class Facility(_ListableONCatResource):
    _RESOURCE_ENDPOINT = "facilities"
    _NAMESPACE = "api"


class Instrument(_ListableONCatResource):
    _RESOURCE_ENDPOINT = "instruments"
    _NAMESPACE = "api"


class Experiment(_ListableONCatResource):
    _RESOURCE_ENDPOINT = "experiments"
    _NAMESPACE = "api"


class ExperimentArchive(_UpdatableONCatSubResource):
    _RESOURCE_ENDPOINT = "experiments"
    _SUB_RESOURCE_ENDPOINT = "archive"
    _NAMESPACE = "api"


class Datafile(
    _CreatableONCatResource, _ListableONCatResource, _RemovableONCatResource
):
    _RESOURCE_ENDPOINT = "datafiles"
    _NAMESPACE = "api"


class DatafileLocation(_CreatableONCatSubResource):
    _RESOURCE_ENDPOINT = "datafiles"
    _SUB_RESOURCE_ENDPOINT = "location"
    _NAMESPACE = "api"


class Reduction(
    _CreatableONCatResource, _ListableONCatResource, _RemovableONCatResource
):
    _RESOURCE_ENDPOINT = "reductions"
    _NAMESPACE = "api"


class ReductionLocation(_CreatableONCatSubResource):
    _RESOURCE_ENDPOINT = "reductions"
    _SUB_RESOURCE_ENDPOINT = "location"
    _NAMESPACE = "api"


class User(_ONCatResource):
    _RESOURCE_ENDPOINT = "users"
    _NAMESPACE = "api"


########################################################################


class Info(_ONCatResource):
    _RESOURCE_ENDPOINT = "info"
    _NAMESPACE = "data"


########################################################################


class CacheEntry(_UpdatableONCatResource):
    _RESOURCE_ENDPOINT = "cache"
    _NAMESPACE = "admin"


class UsageEntry(_ListableONCatResource):
    _RESOURCE_ENDPOINT = "usage"
    _NAMESPACE = "admin"


########################################################################


class Template(
    _CreatableONCatResource, _ListableONCatResource, _RemovableONCatResource
):
    _RESOURCE_ENDPOINT = "templates"
    _NAMESPACE = "settings"


########################################################################
# Client
########################################################################


CLIENT_CREDENTIALS_FLOW = "client"
RESOURCE_OWNER_CREDENTIALS_FLOW = "resource_owner"


class ONCat(object):
    def __init__(
        self,
        url,
        client_id,
        client_secret=None,
        token_getter=None,
        token_setter=None,
        flow=None,
        scopes=None,
    ):
        self._token_getter = token_getter
        self._token_setter = token_setter
        self._client_id = client_id
        self._client_secret = client_secret
        self._url = url
        self._flow = flow
        self._scopes = scopes

        self._token = None
        self._oauth_client = None

        for resource_cls in _ONCatResourceMeta.REGISTERED_RESOURCES:
            setattr(self, resource_cls.__name__, resource_cls(self))

    def get(self, url, **kwargs):
        return self._call_method("get", url, None, **kwargs)

    def put(self, url, data, **kwargs):
        result = self._call_method("put", url, data, **kwargs)

        # Not all resources will return a confirmation representation.
        return result if result != "" else None

    def post(self, url, data, **kwargs):
        return self._call_method("post", url, data, **kwargs)

    def delete(self, url, **kwargs):
        self._call_method("delete", url, None, **kwargs)

    def _call_method(self, method, url, data, **kwargs):
        full_url = (
            self.url() + url if url.startswith("/") else self.url() + "/" + url
        )

        def send_request():
            response = getattr(self.oauth_client(), method)(
                full_url, params=kwargs, json=data, verify=self.should_verify()
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                if error.response.status_code == 404:
                    pyoncat_raise(
                        NotFoundError(
                            'Could not find resource at "%s"' % full_url,
                            original_error=error,
                        )
                    )
                if error.response.status_code == 401:
                    pyoncat_raise(
                        UnauthorizedError(
                            'Not authorized to access "%s"' % full_url,
                            original_error=error,
                        )
                    )
                pyoncat_raise(
                    PyONCatError(
                        'Error: "%s"' % str(error), original_error=error
                    )
                )

            try:
                return response.json()
            except ValueError:
                return response.text

        try:
            return send_request()
        except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as error:
            if (
                self._flow == RESOURCE_OWNER_CREDENTIALS_FLOW
                and "(invalid_grant)" in str(error)
                and "unknown, invalid, or expired refresh token" in str(error)
            ):
                pyoncat_raise(
                    InvalidRefreshTokenError(
                        "It looks like you've tried to use a refresh token "
                        "that has expired.  Not to worry -- this is part of "
                        "the normal OAuth workflow when using refresh tokens, "
                        "since by default (and on a client-by-client basis) "
                        "they are set to expire after a certain length of "
                        "time.  You should be catching this error in your "
                        "client code and then re-prompting the user for their "
                        "username and password so that you may proceed with "
                        "your calls to the ONCat API.\n\n",
                        original_error=error,
                    )
                )
            pyoncat_raise(
                PyONCatError('Error: "%s"' % str(error), original_error=error)
            )
        except oauthlib.oauth2.TokenExpiredError as error:
            if self._flow == CLIENT_CREDENTIALS_FLOW:
                self.login()

                return send_request()

            pyoncat_raise(
                PyONCatError('Error: "%s"' % str(error), original_error=error)
            )

    def oauth_client(self):
        if not self._oauth_client:
            self.login()

        return self._oauth_client

    def get_token(self):
        if self._token_getter is not None:
            return self._token_getter()

        return self._token

    def set_token(self, token):
        if self._token_setter is not None:
            self._token_setter(token)
        else:
            self._token = token

    def should_verify(self):
        if (
            "localhost" in self.url()
            or "load-balancer" in self.url()
            or "proxy" in self.url()
        ):
            # Ignore invalid certs and lack of SSL for OAuth if
            # deploying locally.
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        return (
            "localhost" not in self.url()
            and "load-balancer" not in self.url()
            and "proxy" not in self.url()
        )

    def _auth_headers(self):
        token = self.get_token()
        return {
            "Authorization": "%s %s"
            % (token["token_type"], token["access_token"])
        }

    def url(self):
        return self._url

    def login(self, username=None, password=None):
        if self._flow == CLIENT_CREDENTIALS_FLOW:
            self._login_client_credentials()
        elif self._flow == RESOURCE_OWNER_CREDENTIALS_FLOW:
            self._login_resource_owner_credentials(username, password)
        else:
            assert False

    def _login_client_credentials(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self._oauth_client = requests_oauthlib.OAuth2Session(
                client=oauthlib.oauth2.BackendApplicationClient(
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    scope=self._scopes,
                ),
                scope=self._scopes,
            )
        try:
            token = self._oauth_client.fetch_token(
                self._url + "/oauth/token",
                client_id=self._client_id,
                client_secret=self._client_secret,
                include_client_id=True,
                verify=self.should_verify(),
                scope=self._scopes,
            )
        except oauthlib.oauth2.rfc6749.errors.InvalidClientError as error:
            pyoncat_raise(
                InvalidClientCredentialsError(
                    "You seem to have provided some invalid client "
                    "credentials.  Are you sure they are correct?",
                    original_error=error,
                )
            )

        self.set_token(token)

    def _login_resource_owner_credentials(self, username, password):
        if not username or not password:
            token = self.get_token()
            if not token:
                raise LoginRequiredError(
                    "A username and/or password was not provided when logging "
                    "in."
                )
        else:
            initial_oauth_client = requests_oauthlib.OAuth2Session(
                client=oauthlib.oauth2.LegacyApplicationClient(
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                )
            )

            try:
                token = initial_oauth_client.fetch_token(
                    self._url + "/oauth/token",
                    username=username,
                    password=password,
                    client_id=self._client_id,
                    client_secret=self._client_secret,
                    include_client_id=True,
                    verify=self.should_verify(),
                    scope=self._scopes,
                )
                self.set_token(token)
            except oauthlib.oauth2.rfc6749.errors.InvalidClientError as error:
                pyoncat_raise(
                    InvalidClientCredentialsError(
                        "You seem to have provided some invalid client "
                        "credentials.  Are you sure they are correct?",
                        original_error=error,
                    )
                )
            except oauthlib.oauth2.rfc6749.errors.InvalidGrantError as error:
                if "(invalid_grant)" in str(
                    error
                ) and "username & password" in str(error):
                    pyoncat_raise(
                        InvalidUserCredentialsError(
                            "The user seems to have provided an invalid "
                            "username and/or password.  They should be shown "
                            "an appropriate error message and prompted to try "
                            "again.",
                            original_error=error,
                        )
                    )
                raise error

        auto_refresh_kwargs = {
            "client_id": self._client_id,
            "verify": self.should_verify(),
        }
        if self._client_secret:
            auto_refresh_kwargs["client_secret"] = self._client_secret

        self._oauth_client = requests_oauthlib.OAuth2Session(
            self._client_id,
            token=token,
            scope=self._scopes,
            auto_refresh_url=self._url + "/oauth/token",
            auto_refresh_kwargs=auto_refresh_kwargs,
            token_updater=self.set_token,
        )


########################################################################
# Misc Tools
########################################################################


class InMemoryTokenStore(object):
    def __init__(self):
        self._token = None

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token


class UserConfigFile(object):
    """
    Use this if you like, but I can't promise it won't change in
    future releases...
    """

    def __init__(self, client_name, path=None):
        self._client_name = client_name
        self.path = (
            os.path.join(os.path.expanduser("~"), ".oncatrc")
            if path is None
            else path
        )

    def _content(self):
        with open(self.path, "r") as user_config_file:
            return json.load(user_config_file)

    def client_id(self):
        return self._content()[self._client_name]["client_id"]

    def client_secret(self):
        return self._content()[self._client_name]["client_secret"]

    def token_getter(self):
        return self._content()[self._client_name].get("current_token", None)

    def token_setter(self, token):
        content = self._content()
        content[self._client_name]["current_token"] = token

        with open(self.path, "w") as user_config_file:
            user_config_file.write(
                json.dumps(content, indent=4, sort_keys=True)
            )


########################################################################
# Misc Tools
########################################################################


def _yield_nodes(d, path, include_branches):
    for node in d.keys():
        node_path = "%s.%s" % (path, node) if path else node
        if isinstance(d[node], dict):
            if include_branches:
                yield node_path
            for nested_node_path in _yield_nodes(
                d[node], node_path, include_branches
            ):
                yield nested_node_path
        else:
            yield node_path
