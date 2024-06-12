# LoA repository (prototype)

Created by:

Fetching loa viewer json (loa.json).

```sh
jq -f xform.jq loa.json > loa.new.json

for loa in $(jq "keys | .[]" loa.new.json -r); do jq ".[\"${loa}\"]" loa.new.json > ${loa}.json; done
```
