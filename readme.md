# auto-example-table

This repository contains a [pre-commit][precommit] hook for aggregating a list
of software examples and automatically updating 

[precommit]: https://pre-commit.com

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: ssh://git@bitbucket.global.renesas.com:7999/lpc_cs/auto-example-table.git
    rev: v0.2.0
    hooks:
      - id: auto-example-table
        args:
          - readme.md
```

Optionally changing `readme.md` to reflect the name of the main readme file
(relative to the repository root).

The file passed to this hook must contain the following markers in order to be
updated:

```html
<!---
AUTOMATICALLY GENERATED CONTENT, DO NOT EDIT!
@EXAMPLE_TABLE_BEGIN@
--->
<!---
@EXAMPLE_TABLE_END@
--->
```

Content between `@EXAMPLE_TABLE_BEGIN@` and `@EXAMPLE_TABLE_END@` will be
updated by this hook.

