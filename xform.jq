map(del(._id, .__v, .createdAt, .updatedAt))
| map(. += {adep: (if .adep_ades == "ADEP" then .aerodrome | split(",\\s?"; "x") else null end)})
| map(. += {ades: (if .adep_ades == "ADEP" then null else .aerodrome | split(",\\s?"; "x") end)})
| map(. += {transferType: (if .xc == "A" then "C" elif .xc == "B" then "D" else null end)})
| map(. += {qnh: (if .feet then .aerodrome else null end)})
| map(. += {vertical: false})
| map(. += {fromSector: 
({
  "EBBU": "eb-el",
  "EDGG": "ed",
  "EDMM": "ed",
  "EDUU": "ed",
  "EDWW": "ed",
  "EDYY": "ed",
  "EGPX": "eg",
  "EHAA": "eh",
  "EKDK": "ek",
  "EPWW": "ep",
  "ESMM": "es",
  "LIPP": "li",
  "LKAA": "lk",
  "LOVV": "lo",
  "LSAS": "ls"
}[.from_fir] + "/" + .from_sector)})
| map(. += {toSector: 
({
  "EBBU": "eb-el",
  "EDGG": "ed",
  "EDMM": "ed",
  "EDUU": "ed",
  "EDWW": "ed",
  "EDYY": "ed",
  "EGPX": "eg",
  "EHAA": "eh",
  "EKDK": "ek",
  "EPWW": "ep",
  "ESMM": "es",
  "LIPP": "li",
  "LKAA": "lk",
  "LOVV": "lo",
  "LSAS": "ls"
}[.to_fir] + "/" + .to_sector)})
| map(. += {remarks: .special_conditions})
| map(. += {cop: (if .cop == "LOR" then null else .cop end)})
| map(. += {rfl: null, runways: null, routeBefore: null, routeAfter: null, releases: null})
| map(del(.feet, .aerodrome, .xc, .adep_ades, .special_conditions))
| group_by(.from_fir + "-" + .to_fir)
| map({ key: (.[0].from_fir + "-" + .[0].to_fir), value: ({ agreements: . }) })
| from_entries
| walk(if type == "object" then del(.to_fir, .to_sector, .from_fir, .from_sector) end)
