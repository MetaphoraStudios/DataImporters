# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_source_space_divers_mini.ipynb (unless otherwise specified).

__all__ = ['SpaceDiversMini']

# Cell

from .core import *

import os
import librosa
import string

# Internal Cell

LENGTH_THRESHOLD = 30 # in seconds

def _filter_long_files(files: list[tuple[str, str]]) -> list[str]:
    "Filter out files that are too long."
    return [(path, filename) for path, filename in files
            if librosa.get_duration(filename=os.path.join(path, filename)) <= LENGTH_THRESHOLD]

# Cell

class SpaceDiversMini(Source):
    @property
    def name(self) -> str:
        return "space_divers_mini"

    def get_files(self, root_dir: str) -> list[tuple[str, str]]:
        samples_dir = os.path.join(root_dir, "Samples")
        return _filter_long_files(get_audio_filenames(samples_dir))

    def get_category(self, path: str, filename: str) -> str:
        return "sci-fi"

    def get_labels(self, path: str, filename: str) -> list[str]:
        # Remove the prefix
        title = remove_extension(filename).removeprefix("99S LT ")
        *labels, specific_label = title.split("-")
        labels = [l.strip() for label in labels for l in label.split()]
        # Remove the variant at the end
        specific_label = specific_label.rstrip(string.whitespace + string.ascii_uppercase)
        return labels + [specific_label]