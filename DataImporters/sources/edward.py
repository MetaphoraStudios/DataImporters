# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/08_source_edward_v1.1.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['CLOTHES_PREFIX', 'FOOTSTEPS_PREFIX', 'Edward']

# Cell

#nbdev_comment from __future__ import annotations

from .core import *

import os

CLOTHES_PREFIX = "Clothes_Movement"
FOOTSTEPS_PREFIX = "Footsteps"

# Cell

class Edward(Source):
    @property
    def name(self) -> str:
        return "edward_v1.1"

    def get_files(self, root_dir: str) -> list[tuple[str, str]]:
        samples_dir = os.path.join(root_dir, "WAV")
        return get_audio_filenames(samples_dir)

    def get_category(self, path: str, filename: str) -> str:
        if CLOTHES_PREFIX in filename:
            return CLOTHES_PREFIX
        elif FOOTSTEPS_PREFIX in filename:
            return FOOTSTEPS_PREFIX
        else:
            raise ValueError("Unknown category for filename: " + filename)

    def get_labels(self, path: str, filename: str) -> list[str]:
        # Remove the prefix and extension
        category = self.get_category(path, filename)
        labels = []

        filename = remove_extension(filename).split(category + "_", maxsplit=1)[1]

        if category == FOOTSTEPS_PREFIX:
            # Footsteps start with the type of material
            material, filename = filename.split("_", maxsplit=1)
            labels.append(material)

        step_label = get_footstep_type(filename)
        if step_label is not None:
            labels.append(step_label)

        labels.append(filename)
        return labels