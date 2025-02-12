# VATGER Letters of Agreement

Each agreement is defined by the following properties on a list of `agreements`
in a directory structure of `transferring_fir/receiving_fir/any_file_name.toml`,
i.e. `EDMM/EDUU/south.toml` and `EDMM/EDUU/east.toml` both defining parts of the
LoA for traffic from EDMM to EDUU, split further to increase manageability.

```toml
[[agreements]]
adep = string[] | null
ades = string[] | null
runway = string[] | null
cop = string | null
route_before = string | null
route_after = string | null
level = int | null
transfer_type = "C" | "D" | null
sfl = int | null
level_at = [int, string] | null
qnh = string | null
releases = "C" | "D" | "T" | "F" | null
remarks = string | null
vertical = boolean | null
remarks = string | null
remarks = string | null
from_sector = string
to_sector = string
```

## `adep`

ICAO identifier of departure airports, one of which must match for the agreement
to apply. If `adep` and `ades` are specified one of each must match.

## `ades`

ICAO identifier of destination airports, one of which must match for the agreement
to apply. If `adep` and `ades` are specified one of each must match.

## `runway`

Active runway of one of the airports in `ades` or `adep`.

## `cop`

Coordination point of the agreement, `null` if the agreement shall apply to any
traffic from `from_sector` to `to_sector`.

## `route_before`/`route_after`

Route elements prior to or after the `cop`. This can be an airway or IFPS compatible
route elements: i.e. `"T161"`, `"KOSIX L986 MAG"`

## `level`

Flight level at which the traffic is to be transferred. `null` for traffic that
needs individual coordination.

## `transfer_type`

`"C"` for transfer of traffic climbing to the specified `level`, `"D"` for descending,
`ǹull` for traffic to be at `level`.

## `sfl`

Supplementary flight level, the level out of which the traffic has to be climbing,
descending. (`transfer_type`)

## `level_at`

Additional specification for the location where the traffic has to meet the transfer
conditions:

- `null`: 0.5 \* radar separation to border
- `[-5, "KPT"]`: latest 5 nm prior to `KPT`
- `[15, "MAH"]`: latest 15 nm after `MAH`
- `[0, "RUDNO"]`: latest at or abeam `RUDNO`

## `qnh`

For agreements where traffic is transferred at an altitude, the value of this property
is the ICAO code of the reference QNH, i.e. 8000ft on EDDM QNH:

```toml
[[agreements]]
cop = "TITIG"
level = 80
sfl = 120
ades = ["LOWS"]
transferType = "D"
qnh = "EDDM"
from_sector = "ed/DMSL"
to_sector = "lo/LOWS_APP"
```

## `releases`

If traffic is:

- `"D"`: released for descent
- `"C"`: released for climb
- `"T"`: released for turns
- `"F"`: fully released
- `null`: not released

## `remarks`

Further remarks for more specific releases or conditions.

## `vertical`

Boolean value if the agreement specifies a silent vertical transfer.

## `from_sector`/`to_sector`

Sectors from and to which traffic is transferred, identified by vatglasses file
and key `"file/ID"`, i.e. `"ed/ZUG"`.
