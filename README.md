# httpie-aws-authv4
AWS / Amazon Signature v4 Signing Process authentication plugin for [HTTPie](https://httpie.org/).

## Installation

```
$ pip install --upgrade httpie-aws-authv4
```

You should now see `aws4` under `--auth-type / -A` in `$ http --help` output.

## Usage

### Credentials in default profile/environment variables/instance profile
This authentication plugin looks for credentials in the same [precedence that the AWS CLI tool](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#config-settings-and-precedence) does.

```
$ http --auth-type aws4 https://asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com/dev/test 
```

### Extra arguments
Using the `--auth` parameter, you can specify different kinds of credentials and options
#### Specify credentials on the CLI
Credentials can be specified shorthand as a pair:

```
$ http --auth-type aws4 --auth ACCESSKEYXXX:AWSSECRETKEYXXX https://asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com/dev/test 
```

#### Additional options
Additional options can be injected into `--auth` including above mentioned credentials; these are following with the short option in parantesis:

* access_key (ak)
* secret_key (sk)
* profile (p)
* domain (d)
* service (s)
* region (r)

#### Specify credentials profile on the CLI
You can specify another profile than the default profile:

```
$ http --auth-type aws4 --auth profile=XXX https://asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com/dev/test
```

### Specify service and region
If for some reason you are not hitting the AWS endpoint directly (common with API Gateway), you will need to specify the AWS provided service and region:

```
$ http --auth-type aws4 --auth s=execute-api:r=eu-west-1 https://api.awesomeservice.net/dev/test
$ http --auth-type aws4 --auth service=execute-api:region=eu-west-1 https://api.awesomeservice.net/dev/test
```
### Specify endpoint
Instead of specifying service and region you can specify domain which is then parsed.

```
$ http --auth-type aws4 --auth d=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
$ http --auth-type aws4 --auth domain=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
```
### Specify credentials and endpoint

```
$ http --auth-type aws4 --auth ak=ACCESSKEYXXX:sk=AWSSECRETKEYXXX:d=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
$ http --auth-type aws4 --auth access_key=ACCESSKEYXXX:secret_key=AWSSECRETKEYXXX:domain=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
```

### Specify credentials profile and endpoint

```
$ http --auth-type aws4 --auth p=XXX:d=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
$ http --auth-type aws4 --auth profile=XXX:domain=asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test
```

### Calling AWS services that require extra information

Many AWS services do not require any extra information to be passed other than the URL, such as the following call to the
S3 service which will list all S3 Buckets in the given AWS account:

```
http -A aws4 s3.us-east-1.amazonaws.com
```

However, some AWS services will require extra information to be passed using query string parameters.  By default, ``httpie`` passes
extra parameters as a JSON body. ``httpie`` can be told to pass extra parameters as form fields using the ``-f`` flag like so:

```
$ http -f -A aws4 ec2.us-east-1.amazonaws.com Action=DescribeVpcs Version=2015-10-01
```

where the *Action* and *Version* parameters were passed to the EC2 service to call the **DescribeVpcs** API.

Alternatively instead of using the ``-f`` flag, ``==`` can be used for each parameter like so:

```
$ http -A aws4 ec2.us-east-1.amazonaws.com Action==DescribeVpcs Version==2015-10-01
```

## Credits

All of the heavy lifting (the signing process) is handled by [aws-requests-auth](https://github.com/DavidMuller/aws-requests-auth)
