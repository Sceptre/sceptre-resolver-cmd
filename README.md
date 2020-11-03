# Sceptre shell command resolver

This resolver can be used to execute any shell command.

## Why?

This resolver is handy, because it allows you to dynamically resolve parameters at runtime. The beautiful thing about it is that it's infintely extensible! You can use it to connect any command line tool to Sceptre.

Use it in conjunction with the typical unix tools (cat, cut, grep etc...) or third party ones (vault, op, etc...)

Use the `!rcmd` tag to activate the resolver. You can also use pipe commands, and generic bash (maybe powershell too but I haven't tried it).

The yaml tag `!cmd` is already used by sceptre hooks, unfortunately it wasn't possible to use the same YAML tag for this custom resolver, so the tag `!rcmd` was used instead.

## Installation

```
pip install git+https://github.com/lukeplausin/sceptre-resolver-cmd.git
```

## Usage / Examples

Use the `!rcmd` tag to activate the resolver. You can also use pipe commands, and generic bash (perhaps even powershell but I haven't tested it).

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
# Add a human readable comment with the deployment date
parameters:
  DeployNote: !rcmd echo "Deployed with love by `whoami` on `date`."
```
