<div align="center" style="text-align:center">
  
# Glasswall Rebuild GitHub Action
## Trust Every File

</div>
We are a file regeneration and analytics company, and a leader in the field of CDR: Content Disarm and Reconstruction.



## Motivation
Open-source software is ever expanding and contributers can have malicious intentions. Glasswall Rebuild allows integration into your repository, scan through images, documents and others to inform repository contributers of potentially malicious files.

## Arguments

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
