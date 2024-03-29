# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/11_annotation.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['Annotation', 'create_annotations', 'load_annotations', 'apply_annotations', 'get_annotation_for',
           'delete_row', 'is_deleted']

# Cell

#nbdev_comment from __future__ import annotations

import pandas as pd
from collections import namedtuple

Annotation = namedtuple("Annotation", "replaces deletes")

# Internal Cell

COLUMNS = ["filename", "category", "label", "extra", "source", "version"]
DELETE_KEYWORD = "<delete>"

# Cell

def create_annotations(rows: list[pd.Series] = None) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=COLUMNS)

def load_annotations(annotation_path: str) -> Annotation:
    """Loads the annotations from a csv file."""
    annotations = pd.read_csv(annotation_path)
    return Annotation(annotations.loc[annotations["version"] != DELETE_KEYWORD],
                      annotations.loc[annotations["version"] == DELETE_KEYWORD])

def apply_annotations(annotations: Annotation, metadata: pd.DataFrame) -> pd.DataFrame:
    """Applies the annotations to the metadata (Assumes no duplicates!!)."""
    replaced = metadata.loc[~metadata["filename"].isin(annotations.deletes["filename"])]
    replaced = pd.concat([replaced, annotations.replaces])
    return replaced.drop_duplicates(subset=["filename"], keep="last")

# Cell

def get_annotation_for(annotations: Annotation, filename: str) -> pd.Series:
    if filename in annotations.replaces["filename"].values:
        return annotations.replaces.loc[annotations.replaces["filename"] == filename].iloc[0]
    elif filename in annotations.deletes["filename"].values:
        return annotations.deletes.loc[annotations.deletes["filename"] == filename].iloc[0]
    return None

# Cell

def delete_row(row: pd.Series) -> pd.Series:
    """Deletes a row from the annotations DataFrame."""
    row = row.copy()
    row[5] = DELETE_KEYWORD
    return row

def is_deleted(row: pd.Series) -> bool:
    """Returns whether a row is deleted."""
    return row[5] == DELETE_KEYWORD