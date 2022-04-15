from unittest.mock import Mock

import httpie_aws_authv4
import pytest


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
    m = Mock()
    m.access_key = "mock_access_key"
    m.secret_key = "mock_secret_key"
    m.token = "mock_token"

    class MockSession(Mock):
        def get_credentials(self):
            return m

    mocker.patch("httpie_aws_authv4.session.Session", MockSession)

    auth = httpie_aws_authv4.AWSv4AuthPlugin()
    auth.raw_auth = input
    res = auth.get_auth()

    assert res.aws_access_key == "mock_access_key"
    assert res.aws_secret_access_key == "mock_secret_key"
    assert res.aws_token == "mock_token"

    for attribute, value in expected_extra.items():
        assert getattr(res, attribute) == value


@pytest.mark.parametrize(
    "input,expected",
    [
        ("", {}),
        ("profile=XXX", {}),
        ("p=XXX", {}),
        ("service=XXX", {"aws_service": "XXX"}),
        ("s=XXX", {"aws_service": "XXX"}),
        ("region=XXX", {"aws_region": "XXX"}),
        ("r=XXX", {"aws_region": "XXX"}),
        ("domain=XXX", {"domain": "XXX"}),
        ("d=XXX", {"domain": "XXX"}),
        ('access_key=XXX', {"aws_access_key": "mock_access_key"}),
        (
            'access_key=XXX,secret_key=YYY',
            {"aws_access_key": "XXX", "aws_secret_access_key": "YYY"},
        ),
        (
            'ak=XXX,sk=YYY',
            {"aws_access_key": "XXX", "aws_secret_access_key": "YYY"},
        ),
        ("service=XXX,region=YYY", {"aws_service": "XXX", "aws_region": "YYY"}),
        ("s=XXX,r=YYY", {"aws_service": "XXX", "aws_region": "YYY"}),
    ],
)
def test_auth_parsing_comma_separated(mocker, input, expected):
    m = Mock()
    m.access_key = "mock_access_key"
    m.secret_key = "mock_secret_key"
    m.token = "mock_token"

    class MockSession(Mock):
        def get_credentials(self):
            return m

    mocker.patch("httpie_aws_authv4.session.Session", MockSession)

    auth = httpie_aws_authv4.AWSv4AuthPlugin()
    auth.raw_auth = input
    res = auth.get_auth()

    print(res)

    for attribute, value in expected.items():
        assert getattr(res, attribute) == value
