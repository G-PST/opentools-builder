# GPST data validator github action. 

This action prints validates the content of `g-pst/opentools` repo.

## Inputs

## `datapath`

**Required** Name of the folder where all the data exists.

## Outputs

## `exitcode`

Exit code returned by pytest.

## Example usage

```yaml
uses: g-pst/opentools-validation@v1.3.0
with:
  datapath: 'data'
```

