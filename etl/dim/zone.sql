create table dim_zone (
  "id"    UInt8,
  "name"  String
) ENGINE = MergeTree()
order by cve_loc;