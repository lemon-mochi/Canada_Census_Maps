Idea: the main table should have DGUID, CHARACTERISTIC_ID, C1_COUNT_TOTAL, C2_COUNT_MEN+, C3_COUNT_WOMEN+, C10_RATE_TOTAL, C11_RATE_MEN+, C12_RATE_WOMEN+.

Have two more tables that connect DGUID to GEO_LEVEL and GEO_NANE, and then another that connects CHARACTERISTIC_ID to CHARACTERISTIC_NAME.

Have a table that connects CHARACTERISTIC_ID with the columns that CHARACTERISTIC_ID has.