# pubMLST Client

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

#### Example Output

| name          | id |    description | locus_count | records | last_added | last_updated |
|:------------- | --:|:-------------- | -----------:| -------:| ----------:| ------------:|
| achromobacter |  1 | MLST           |           7 |     480 | 2020-02-20 |   2020-02-20 |
| abaumannii    |  1 | MLST (Oxford)  |           7 |    2088 | 2020-02-07 |   2020-02-07 |
| abaumannii    |  2 | MLST (Pasteur) |           7 |    1438 | 2020-02-18 |   2020-02-18 |
| aeromonas     |  1 | MLST           |           6 |     656 | 2020-01-07 |   2020-01-08 |


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
