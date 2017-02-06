# httpie-aws-authv4
AWS / Amazon Signature v4 Signing Process authentication plugin for [HTTPie](https://httpie.org/).

## Installation

```
$ pip install --upgrade httpie-aws-authv4
```

You should now see `aws4` under `--auth-type / -A` in `$ http --help` output.

## Usage

### Credentials in default profile/environment variables/instance profile
This authentication plugin looks for credentials in the same [precedence that the AWS CLI tool](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#config-settings-and-precedence) does.  At the moment, the plugin only looks at the default profile for credentials stored in credentials file.

```
$ http --auth-type aws4 https://asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com/dev/test 
```

### Specify credentials on the CLI

```
$ http --auth-type aws4 --auth ACCESSKEYXXX:AWSSECRETKEYXXX https://asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com/dev/test 
```

### Specify the endpoint
If for some reason you are not hitting the AWS endpoint directly (common with API Gateway), you will need to specify the AWS provided endpoint on the CLI.  This is used to determine the service and region values required for the signature process.

```
$ http --auth-type aws4 --auth asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test 
```

### Specify credentials and endpoint

```
$ http --auth-type aws4 --auth ACCESSKEYXXX:AWSSECRETKEYXXX:asdf123a9sas.execute-api.ap-southeast-2.amazonaws.com https://api.awesomeservice.net/dev/test 
```

## Credits

All of the heavy lifting (the signing process) is handled by [aws-requests-auth](https://github.com/DavidMuller/aws-requests-auth)
