# Sceptre shell command resolver

This resolver can be used to execute any shell command.

## Why?

This resolver is handy, because it allows you to dynamically resolve parameters at runtime.
The beautiful thing about it is that it's infintely extensible! You can use it to connect
any command line tool to Sceptre.

Use it in conjunction with the typical unix tools (cat, cut, grep etc...) or third party
ones (vault, op, etc...)

Use the `!rcmd` tag to activate the resolver. You can also use pipe commands, and generic
bash (maybe powershell too but I haven't tried it).

The yaml tag `!cmd` is already used by sceptre hooks, unfortunately it wasn't possible to use
the same YAML tag for this custom resolver, so the tag `!rcmd` was used instead.

## Installation

```
# To install directly from PyPI
pip install sceptre-cmd-resolver

# To install from this git repo
pip install git+https://github.com/Sceptre/sceptre-resolver-cmd.git
```

## Usage / Examples

Use the `!rcmd` tag to activate the resolver. You can also use pipe commands, and generic
bash (perhaps even powershell but I haven't tested it).

```yaml
# Resolve the contents of a file with cat
parameters:
  DatabasePassword: !rcmd cat .env/dev/password
```

```yaml
# Resolve data from a json file with cat + jq
parameters:
  DatabasePassword: !rcmd cat .env/data | jq -r '.Passwords.dev'
```

```yaml
# Resolve a secret in vault using the vault CLI (you must be logged in!)
parameters:
  DatabasePassword: !rcmd vault kv get -field=password myapp/database/dev
```

```yaml
parameters:
  # Resolve the EC2 AMI Image ID to the latest official version of Ubuntu 20.04 at deploy time
  EC2ImageIdUbuntu: !rcmd >-
    aws ssm get-parameters
      --region eu-west-2
      --names /aws/service/canonical/ubuntu/server/20.04/stable/current/amd64/hvm/ebs-gp2/ami-id
      --query 'Parameters[0].[Value]' --output text

  # Resolve the EC2 AMI Image ID to the latest official version Windows Server 2019 at deploy time
  EC2ImageIdWindows: !rcmd >-
    aws ssm get-parameters
      --region eu-west-2
      --names /aws/service/ami-windows-latest/Windows_Server-2019-English-Full-Base
      | jq -r '.Parameters[0].Value' | jq -r '.image_id'
```

```yaml
# Add a human readable comment with the deployment date
parameters:
  DeployNote: !rcmd echo "Deployed by `whoami` on `date` :-)"
```

```yaml
# Execute the command with the same AWS profile provided to Sceptre
parameters:
  CanonicalUserId: !rcmd
    command: "aws s3api list-buckets --query Owner.ID --output text"
```

```yaml
# Override the command execution with a specific AWS profile, region, and/or sceptre_role
parameters:
  CanonicalUserId: !rcmd
    command: "aws s3api list-buckets --query Owner.ID --output text"
    profile: "my-profile"
    region: "us-west-2"
    sceptre_role: "arn:aws:iam::123456:role/my-role-to-override-the-stack-role"
```
