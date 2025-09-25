# auto-example-table

This repository contains a program for aggregating a list of software examples
and automatically updating a generated table, and a [pre-commit][precommit]
hook to automate the process of keeping said list up-to-date.

[precommit]: https://pre-commit.com

## Repo setup

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/renesas/auto-example-table
    rev: v0.4.2
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

## Example setup

This program recusively scans for markdown readme files (matching names listed
in [consts.py][consts]) with [front matter][frontmatter].
The following properties are supported:

|Variable|Type|Description|
|-|-|-|
|`name`|`str`|Example **project** name.|
|`boards`|`list[str]`|A list of supported boards. See `BOARDS` in [consts.py][consts] for a list of board aliases.|
|`keywords`|`list[str]`|A list of keywords. Appended to the end of the description if present.|
|`description`|`str`|A short description of the example|

[frontmatter]: https://jekyllrb.com/docs/front-matter
[consts]: auto_example_table/consts.py

