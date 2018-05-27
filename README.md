print-env
===

[![Build Status](https://travis-ci.org/woozyking/print-env.svg?branch=master)](https://travis-ci.org/woozyking/print-env)

CLI to print environment variables from supported files.

This is derived from projects that:

- Use environment variables as the main interface for configuration
- Use source-control ignored files to store environment variables for scenarios such as local development

## Install

```bash
$ pipenv install print-env
# or
$ pip install print-env
```

## Usage

Assume a `.env` file that contains the following content:

```bash
# .env
FLASK_APP=app.py
FLASK_DEBUG=1
SQL_URI=<SQL connection string that may contain credentials>
# and more...
```

Then simply

```bash
$ print-env
FLASK_APP=app.py FLASK_DEBUG=1 SQL_URI=<redacted> # and more...
```

The above would print out environment variables stored in `.env`, or `env.yml`, or `env.json` (roughly attempted in this order). You can also exclusively specify the file:

```bash
$ print-env /path/to/env/file.yml
```

and the script would attempt to parse the file based on its extension given. Note that any file extension that is not of YAML or JSON type is attempted as a dotenv file.

In fact, you can specify a series of files. Note that in case of duplicates, the last files take precedence, for example:

```bash
# content of base.env
LOG_LVL=warning
API_TOKEN=aabbcc
```

```bash
# content of dev.env
LOG_LVL=debug
```

```bash
$ print-env base.env dev.env
LOG_LVL=debug API_TOKEN=aabbcc
```

Another common case is when an external file is used to supply environment variables at _deploy-time_, for example, when used with the [serverless framework](https://github.com/serverless/serverless) with a `serverless.yml` that may look like:

```yaml
service: env-vars

package:
  exclude:
    - node_modules/**
    - '*env.yml'
    - Pipefile
    - Pipfile.lock

functions:
  test:
    # test.py - handler()
    handler: test.handler
    # sourcing env vars from ./env.yml
    environment: ${file(./env.yml):}
```

and for local test runs you can utilize `print-env` to reuse the same `env.yml`:

```bash
$ env $(print-env) python test.py  # omitted file path since env.yml is on the default try-list
```

Similarly, `print-env` can be used for _build-time_ configuration. For example, with an imaginary client-side project with a `package.json` that may look like:

```json
{
  "name": "TestApp",
  "version": "1.0.1",
  "scripts": {
    "build": "env $(print-env local-env.json) parcel build index.html",
    "build:dev": "env $(print-env dev-env.json) parcel build index.html",
    "build:prod": "env $(print-env prod-env.json) parcel build index.html"
  }
}
```
