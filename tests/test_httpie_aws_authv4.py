import pytest
import mock

import httpie_aws_authv4


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            "ACCESSKEYXXX:AWSSECRETKEYXXX",
            httpie_aws_authv4.AWSAuth(
                access_key="ACCESSKEYXXX", secret_key="AWSSECRETKEYXXX"
            ),
        ),
        (
            "ACCESSKEYXXX:AWSSECRETKEYXXX:asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com",
            httpie_aws_authv4.AWSAuth(
                access_key="ACCESSKEYXXX",
                secret_key="AWSSECRETKEYXXX",
                domain="asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com",
            ),
        ),
    ],
)
def test_auth_parsing_static_keys(input, expected):
    auth = httpie_aws_authv4.AWSv4AuthPlugin()
    auth.raw_auth = input
    assert auth.get_auth() == expected


@pytest.mark.parametrize(
    "input,expected_profile,expected_extra",
    [
        ("", "", {}),
        ("profile:XXX", "XXX", {}),
        (
            "profile:XXX:asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com",
            "XXX",
            {"domain": "asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com"},
        ),
    ],
)
def test_auth_parsing_profile(mocker, input, expected_profile, expected_extra):
    m = mock.Mock()
    m.access_key = "mock_access_key"
    m.secret_key = "mock_secret_key"
    m.token = "mock_token"

    class MockSession(mock.Mock):
        def get_credentials(self):
            return m

    mocker.patch("httpie_aws_authv4.session.Session", MockSession)

    auth = httpie_aws_authv4.AWSv4AuthPlugin()
    auth.raw_auth = input
    res = auth.get_auth()

    print(res.aws_access_key)

    assert res.aws_access_key == "mock_access_key"
    assert res.aws_secret_access_key == "mock_secret_key"
    assert res.aws_token == "mock_token"

    for attribute, value in expected_extra.items():
        assert getattr(res, attribute) == value
