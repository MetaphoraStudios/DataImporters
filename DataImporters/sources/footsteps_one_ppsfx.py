# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_source_footsteps_one_ppsfx_004.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['FootstepsOnePpsfx']

# Cell

#nbdev_comment from __future__ import annotations

from .core import *

import os
import pandas as pd

# Cell

class FootstepsOnePpsfx(Source):
    def preload(self, root_dir: str):
        metadata_path = os.path.join(root_dir,
            "Documents", "PPSFX 004 - Footsteps One Metadata.xls")
        self.extra_metadata = pd.read_excel(metadata_path)

    @property
    def name(self) -> str:
        return "footsteps_one_ppsfx_004"

    def get_files(self, root_dir: str) -> list[tuple[str, str]]:
        samples_dir = os.path.join(root_dir, "Audio")
        return get_audio_filenames(samples_dir)

    def get_category(self, path: str, filename: str) -> str:
        return "footsteps"

    def get_labels(self, path: str, filename: str) -> list[str]:
        # Remove the prefix
        filename = remove_prefix(remove_extension(filename), "Footsteps")

        # Remove number at the end of the filename
        filename = filename.rsplit("0", maxsplit=1)[0]

        # For each step type, we remove it from the filename and add it to the labels
        labels = []

        step_label = get_footstep_type(filename)
        if step_label is not None:
            filename = filename.lower().replace(" " + step_label, "")
            labels.append(step_label)

        labels.append(filename)

        return labels

    def get_extra(self, path: str, filename: str) -> str:
        row = self.extra_metadata.loc[self.extra_metadata["Filename"] == filename]
        return row["BWDescription"].values[0]