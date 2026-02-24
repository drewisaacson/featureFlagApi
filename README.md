Run locally:
- `make install`
- `make build`
- `make run`

Example feature creation:
```
> curl -X POST <endpoint>/feature   -H "Content-Type: applicatio
n/json"   -d '{
    "feature_name": "my-feature",
    "value": "enabled",
    "feature_description": "My test feature"
  }'

{"status":"accepted","feature":{"feature_name":"my-feature","value":"enabled","feature_description":"My test feature","timestamp":"2026-02-24T19:29:47.548089"}}
```