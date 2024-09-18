import pandas as pd

"""
This script processes the affiliations column from Author.csv, cleans it, and writes the result to a file.
"""

authors = pd.read_csv("Author.csv", index_col=0)
affs = pd.DataFrame(authors['Affiliation'])

affs['Affiliation'] = affs['Affiliation'].str.strip().str.lower()

# Replace special characters and symbols
replacements = {
    "\xe2\x80\x99": "'", "\xc2\xa8\xc2\xa2": "a", "\xc2\xa8": "", "\xc3\xa8": "e",
    "\xc3\xad": "i", "\xc3\xa4": "a", "\xc3\xaa": "e", "\xc3\xa3": "a", "\xc3\xb3": "o",
    "\xc3\xb6": "0", "\xc3\x96": "o", "\xc3\xaf": "i", "\xc3\xb8": "o", "\xc3\xba": "u",
    "\xc3\x85": "a", "\xc3\x89": "e", "\xc3\xa9": "e", "\xc3\x9c": "u", "\xc3\xbc": "u",
    "\xc3\xb1": "n", "\xc3\xb4": "o", "\xc3\xa1": "a", "\xc3\xa7": "c", "\xc3\x9f": "b",
    "\xc3\xb5": "o", "\xc3\xa5": "a", "\xc3\xa0": "a", "\xc3\xab": "e", "\xc3\xb2": "o",
    "\xc5\x81": "l"
}
for old, new in replacements.items():
    affs['Affiliation'] = affs['Affiliation'].str.replace(old, new)

# Remove unwanted characters and generic/common terms
affs['Affiliation'] = affs['Affiliation'].replace(
    ['|', ',', '"', '\'', '(', ')', '.', ';', '-', '&'], ' ', regex=True
).replace(
    [' inc', ' for ', ' fur ', ' et ', ' a ', ' and ', ' und ', ' y ', ' at ', ' in ', ' of ', ' von ', ' des ', ' de ', ' di ', ' 1 '], ' ', regex=True
).replace(
    ['^the ', '^las ', '^la ', '^il ', '^el ', '^los ', '^der '], '', regex=True
).replace(
    [' the ', ' las ', ' la ', ' il ', ' el ', ' los ', ' der '], ' ', regex=True
).replace(
    ['institute', 'institut', 'science', 'research', 'center', 'national', 'nacional', 'department', 'dept', 'departamento', 'dipartimento', 'university', 'universidad', 'universitat', 'universiteit', 'technische', 'technology', 'laboratory', 'corporation', 'usa', 'school', 'college', 'state', 'group', 'division', 'faculty', 'faculdad', 'universidade', 'faculdade', 'federal', 'depto'], '', regex=True
).replace(
    [' new ', ' st '], ' ', regex=True
).replace(
    ['^[0-9] ', ' [0-9] ', '^[a-z] ', ' [a-z] '], '', regex=True
)

affs = affs[pd.notnull(affs['Affiliation']) & (affs['Affiliation'] != '') & (affs['Affiliation'] != ' ')]

# Print and save results
print(len(affs.index))
affs['Affiliation'] = affs['Affiliation'].str.split()
affs['Affiliation'].to_csv('affs_loose.tsv', sep='\t', header=['Affiliation'])

