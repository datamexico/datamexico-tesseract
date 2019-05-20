create table geography (
    "cve_ent"     String
    "name_ent"    String
    "cve_mun"     String
    "name_mun"    String
    "cve_loc"     String
    "name_loc"    String
    "latitude"    String
    "longitude"   String
    "altitude"    String
) ENGINE = MergeTree()
order by cve_loc;