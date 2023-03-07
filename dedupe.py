import pandas as pd
from pathlib import Path

# file_withDupes - filename of original file 
# file_withoutDupes - filename of file with (blanks and) duplicates removed
# file_blankRecords - filename of file with records where dedupeField is blank
# file_dupeRecords - filename of file with records where dedupefield is not blank and is a duplicate of an existing
# df_withDupes - data frame of original file
# df_withoutDupes - data frame with duplicates removed
# df_dupeRecordsMask - data frame of boolean mask indicating which rows are duplicate 
# df_dupeRecords - data frame of records identified as the duplicates

# set values here

# get the name of the original file
file_withDupes = Path(input(f"\nEnter filename\n"))

# get the name of the column to check for duplicates
dedupeField = input(f"\nEnter name of column to check for duplicates\n")

# get whether to keep first or last record as the master
keepRecord = input(f"\nEnter record to keep. Valid values are 'first' or 'last'\n")

# file without dupes will be named [file_withDupes]_deduped_on[DupeField]_keep[keepRecord].csv
file_withoutDupes = file_withDupes.stem + '_deduped_on' + dedupeField.title().replace(" ", "") + '_keep' + keepRecord.capitalize() + '.csv'

# file of records with blank dedupeField will be named [file_withDupes]_deduped_on[DupeField]_keep[keepRecord]_blankRecords.csv
file_blankRecords = file_withDupes.stem + '_deduped_on' + dedupeField.title().replace(" ", "") + '_keep' + keepRecord.capitalize() + '_blankRecords' + '.csv'

# file of duplicate records will be named [file_withDupes]_deduped_on[DupeField]_keep[keepRecord]_dupeRecords.csv
file_dupeRecords = file_withDupes.stem + '_deduped_on' + dedupeField.title().replace(" ", "") + '_keep' + keepRecord.capitalize() + '_dupeRecords' + '.csv'

print(file_withoutDupes)
print(file_blankRecords)
print(file_dupeRecords)

# read the original file into a dataframe df_withDupes
df_withDupes = pd.read_csv(file_withDupes)
print(df_withDupes)

# create a dataframe with records where dedupeField is not blank/NaN since these will all be considered "duplicates"
df_withoutBlanks = df_withDupes.dropna(subset=[dedupeField])
print(df_withoutBlanks)

#create a boolean mask indicating which records have a blank dedupeField
df_blankDedupeFieldRecordsMask = df_withDupes[dedupeField].isna()
print(df_blankDedupeFieldRecordsMask)

# apply boolean mask to original file to create dataframe of only the records with a blank dedupeField
df_blankDedupeFieldRecords = df_withDupes[df_blankDedupeFieldRecordsMask]
print(df_blankDedupeFieldRecords)

# write the above dataframe of records with a blank dedupeField to a csv
df_blankDedupeFieldRecords.to_csv(file_blankRecords,index=False)

# create a dataframe without dupes, by dedupeField, and keeping the keepRecord
df_withoutDupes = df_withoutBlanks.drop_duplicates(subset=[dedupeField], keep=keepRecord)
print(df_withoutDupes)

# write the unique records (duplicates removed) to a csv
df_withoutDupes.to_csv(file_withoutDupes, index=False)

#create a boolean mask indicating which records are duplicate
df_dupeRecordsMask = df_withoutBlanks.duplicated(subset=[dedupeField], keep=keepRecord)
print(df_dupeRecordsMask)

#apply boolean mask to original file to create dataframe of only the duplicate records (not including the "kept" record)
df_dupeRecords = df_withoutBlanks[df_dupeRecordsMask]
print(df_dupeRecords)

# write the above dataframe of duplicate records to a csv
df_dupeRecords.to_csv(file_dupeRecords,index=False)



