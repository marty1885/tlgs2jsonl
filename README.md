# tlgs2jsonl

Convert TLGS database to jsonl format.

### How to use

1. Connect to your TLGS database and dump the `content_body` and `raw_content_hash` from table `pages`

```sql
> psql -h localhost -U postgres -d tlgs -c "COPY (SELECT content_body, raw_content_hash FROM pages) TO STDOUT WITH CSV HEADER DELIMITER E'\t'" > tlgs.csv
```

2. Run the script

```bash
> python tlgs2jsonl.py --source tlgs.csv --output tlgs.jsonl
```

You are done