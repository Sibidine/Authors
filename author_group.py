import pandas as pd
import numpy as np
import time

start_time = time.time()

"""
This script finds "duplicate papers" and creates groupings of all authors who have authored these papers.
"""

####################################################################################
# Load data
####################################################################################
authors = pd.read_csv("Author.csv")
papers = pd.read_csv("Paper.csv")
author_papers = pd.read_csv("PaperAuthor.csv")

####################################################################################
# Remove author paper duplicates and not in author set
####################################################################################
author_papers = author_papers[['AuthorId', 'PaperId']].drop_duplicates()
author_papers = author_papers[author_papers.AuthorId.isin(authors.Id)]
author_papers = author_papers.sort_values(['AuthorId', 'PaperId'])

####################################################################################
# Clean paper title
####################################################################################
papers = papers.drop(['Year', 'ConferenceId', 'JournalId', 'Keyword'], axis=1)
papers['Title'] = papers['Title'].str.lower().str.replace(r"[^a-z0-9]", " ").str.replace(r"\s+", " ").str.strip()
papers = papers[papers.Id.isin(author_papers.PaperId)]
papers = papers[pd.notnull(papers['Title'])]
papers = papers[papers['Title'].str.len() > 10].sort_values('Id')

####################################################################################
# Mark duplicate papers
####################################################################################
paper_alias = papers.groupby('Title').groups

papers['PaperAliasId'] = -1
papers['PaperAliasSize'] = -1
for title, alias_ix in paper_alias.items():
    papers.loc[alias_ix, 'PaperAliasId'] = papers.loc[alias_ix[0], 'Id']
    papers.loc[alias_ix, 'PaperAliasSize'] = len(alias_ix)

papers = papers[papers['PaperAliasSize'] > 1]

####################################################################################
# Join datasets and calculate groups
####################################################################################
author_groups = pd.merge(author_papers, papers, left_on='PaperId', right_on='Id').drop(['Id', 'PaperAliasSize', 'Title'], axis=1)
author_groups = pd.merge(author_groups, authors, left_on='AuthorId', right_on='Id').drop(['Id', 'Affiliation'], axis=1)
author_groups = author_groups.sort_values(['PaperAliasId', 'PaperId', 'AuthorId'])

author_groups_grouped = author_groups.groupby('PaperAliasId').groups
author_groups['KeepRecord'] = False

for alias_id, alias_ix in author_groups_grouped.items():
    author_unique = ~author_groups.loc[alias_ix].duplicated('AuthorId').values
    paper_set = set()
    for ix in range(len(alias_ix)):
        cur_paper = author_groups.loc[alias_ix[ix], 'PaperId']
        if author_unique[ix] and cur_paper not in paper_set:
            paper_set.add(cur_paper)
            if len(paper_set) > 1:
                break
    if len(paper_set) > 1:
        author_groups.loc[alias_ix[author_unique], 'KeepRecord'] = True

author_groups = author_groups[author_groups['KeepRecord']].drop(['KeepRecord'], axis=1)

author_groups_csv = author_groups[['PaperAliasId', 'AuthorId', 'PaperId', 'Name']]
author_groups_csv.columns = ["authorgroup", "authorid", "subgroupid", "a_name"]
author_groups_csv.to_csv("author_groups.csv", header=["authorgroup", "authorid", "subgroupid", "a_name"], index=False)

print("Total time", time.time() - start_time, "seconds")

