# pubMLST Download Script

## Usage

### List available schemes

```
usage: pubmlst_list [-h] [--pattern PATTERN] [--names_only]

optional arguments:
  -h, --help            show this help message and exit
  --pattern PATTERN, -p PATTERN
                        regex pattern to filter scheme names
  --names_only, -n      Only show scheme names
```

### Download schemes

```
usage: pubmlst_download [-h] [--scheme_name SCHEME_NAME]
                        [--scheme_id SCHEME_ID] [--outdir OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  --scheme_name SCHEME_NAME, -s SCHEME_NAME
                        scheme name
  --scheme_id SCHEME_ID, -i SCHEME_ID
                        scheme id
  --outdir OUTDIR, -o OUTDIR
                        output directory
```