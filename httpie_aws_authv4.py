# -*- coding: utf-8 -*-
"""
AWS-v4 auth plugin for HTTPie.

"""
import re

from aws_requests_auth.aws_auth import AWSRequestsAuth
from boto3 import session
from httpie.plugins import AuthPlugin
from urllib3.util import parse_url

__version__ = "0.3.0"
__author__ = "Aidan Rowe"
__licence__ = "MIT"


class AWSAuth(object):
    def __init__(
        self,
        access_key=None,
        secret_key=None,
        domain=None,
        profile=None,
        region=None,
        service=None,
    ):
        self.domain = domain
        self.aws_region: str = region
        self.aws_service: str = service

        if access_key and secret_key:
            self.aws_access_key = access_key
            self.aws_secret_access_key = secret_key
            self.aws_token = None
        else:
            sess = session.Session(profile_name=profile)
            creds = sess.get_credentials()

            self.aws_access_key = creds.access_key
            self.aws_secret_access_key = creds.secret_key
            self.aws_token = creds.token

    def __eq__(self, other):
        if not isinstance(other, AWSAuth):
            raise NotImplementedError

        return all(
            [
                self.aws_access_key == other.aws_access_key,
                self.aws_secret_access_key == other.aws_secret_access_key,
                self.aws_token == other.aws_token,
                self.domain == other.domain,
                self.aws_region == other.aws_region,
                self.aws_service == other.aws_service,
            ]
        )

    def __call__(self, r):
        try:
            # Host used in signature *MUST* always match with Host HTTP header.
            host = r.headers.get("Host")
            if not host:
                _, _, host, _, _, _, _ = parse_url(r.url)
                r.headers["Host"] = host

            if self.aws_region is not None and self.aws_service is not None:
                aws_params = dict(region=self.aws_region, service=self.aws_service)
            elif self.domain is not None:
                aws_params = self._parse_url(self.domain)
            else:
                aws_params = self._parse_url(host)
        except ValueError:
            print("ERROR: Could not parse neccessary information from URL.")
            raise
        except Exception as error:
            print("Error parsing URL: %s" % error)
            raise

        aws_request = AWSRequestsAuth(
            aws_access_key=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_host=host,
            aws_region=aws_params["region"],
            aws_service=aws_params["service"],
            aws_token=self.aws_token,
        )

        return aws_request.__call__(r)

    @staticmethod
    def _parse_url(domain):
        p = re.compile(r"([^\.]+)\.es\.amazonaws.com(\.cn)?$")
        m = p.search(domain)

        if m:
            return {"region": m.group(1), "service": "es"}

        p = re.compile(r"([^\.]+)\.([^\.]+)\.amazonaws.com(\.cn)?$")
        m = p.search(domain)

        if m:
            return {"region": m.group(2), "service": m.group(1)}

        raise ValueError("Could not determine AWS region or service from domain name.")


class AWSv4AuthPlugin(AuthPlugin):
    name = "AWS auth-v4"
    auth_type = "aws4"
    description = "Sign requests using the AWS Signature Version 4 Signing Process"
    auth_require = False
    auth_parse = False
    prompt_password = False

    alias_params = {
        "ak": "access_key",
        "sk": "secret_key",
        "p": "profile",
        "d": "domain",
        "s": "service",
        "r": "region",
    }
    """map of alias -> full param name"""

    def get_auth(self, username=None, password=None):
        """
        To remain consistant with AWS tools, boto3 credential store is used
        to retrieve the users API keys.  This means environment variables
        take precedent over ~/.aws/credentials and IAM roles.  credentials
        can be provided on the CLI using the -a flag eg,
            -a <access_key>:<secret_access_key>

        You can also provide aditional parameters using following syntax:
            -a access_key=<access_key>,secret_key=<secret_key>,
            profile=<profile>,domain=<domain>,service=<service>,region=<region>

        or short equvivalent:
            -a ak=<access_key>,sk=<secret_key>,p=<profile>,d=<domain>,
            s=<service>,r=<region>

        For example:
            -a s=executeapi,r=eu-west-1

        An attempt is made to try and determine the region, endpoint and
        service from a given request URL if you are not supplying this data as above.
        If you are using a custom domain this will fail and service plus region need
        to be supplied in the -a flag.
        """

        params: dict = {}

        if self.raw_auth is not None:

            try:
                if "=" in self.raw_auth:

                    params = dict(x.split("=", 2) for x in self.raw_auth.split(","))

                    for alias, full in self.alias_params.items():
                        if alias in params:
                            params[full] = params[alias]
                            del params[alias]

                else:

                    parts = self.raw_auth.split(":")
                    if len(parts) >= 2:
                        if parts[0] == "profile":
                            params["profile"] = parts[1]
                        else:
                            params["access_key"] = parts[0]
                            params["secret_key"] = parts[1]
                        if len(parts) == 3:
                            params["domain"] = parts[2]
                    elif len(parts) == 1:
                        params["domain"] = parts[0]

            except ValueError:
                print("ERROR: Could not parse auth string.")
                raise

        return AWSAuth(**params)
