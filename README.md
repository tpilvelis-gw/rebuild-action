# Glasswall Rebuild GitHub Action

This action prints "Hello World" or "Hello" + the name of a person to greet to the log.

## Usage
uses: tpilvelis-gw/rebuild-action@v1
with:
  filetype: 'png'

## Arguments
Glasswall Rebuild Github Action currently supports:
| Filetype |
|---|
| png |

Glasswall Rebuild GitHub Action currently supports one input from the user: `filetype`

| Input  | Description | Usage |
| :---:     |     :---:   |    :---:   |
| `filetype`  | Extension of the files to scan in the repository  | Required |

### Example `workflow.yml` with Glasswall Rebuild Github Action
```yaml
name: Example workflow for Glasswall Rebuild
on: [push]

jobs:
  CI_Pipeline:
    runs-on: ubuntu-latest
    name: Pipeline Using Glasswall Rebuild
    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v2

      - name: Glasswall Rebuild
        uses: tpilvelis-gw/rebuild-action@v1
        with:
          filetype: 'png'
```
