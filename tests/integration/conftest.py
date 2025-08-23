query_insert_note = (
    "INSERT INTO notes"
    " (oid, bedtime_date, owner_oid, went_to_bed, fell_asleep, woke_up, got_up,"
    " no_sleep)"
    " VALUES ("
    " :oid, :bedtime_date, :owner_oid, :went_to_bed, :fell_asleep, :woke_up,"
    " :got_up, :no_sleep);"
)
