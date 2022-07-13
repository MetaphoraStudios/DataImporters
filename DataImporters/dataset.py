# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_dataset.ipynb (unless otherwise specified).

__all__ = ['Dataset']

# Cell

from .sources.core import Source, process

import os
import shutil
import pandas as pd

# Internal Cell

def _sync_audio_files(source_dir: str, target_dir: str):
    """Synchronises audio files from source_dir to target_dir. Only copying new files."""
    for filename in os.listdir(source_dir):
        if filename.endswith(".wav"):
            target_file_path = os.path.join(target_dir, filename)
            if not os.path.exists(target_file_path):
                shutil.copy2(os.path.join(source_dir, filename), target_file_path)

# Cell

class Dataset:
    def __init__(self, sources: list[Source], data_path: str):
        self.sources = sources
        self.data_path = data_path
        self.intermediate_path = os.path.join(data_path, "intermediate/")
        self.output_path = os.path.join(data_path, "dataset/")
        self.audio_output_path = os.path.join(self.output_path, "audio/")
        self.metadata_output_path = os.path.join(self.output_path, "metadata.csv")

    def _prepare_output(self):
        if not os.path.exists(self.audio_output_path):
            os.makedirs(self.audio_output_path)

    def _compile_source(self, source: str):
        source_path = os.path.join(self.intermediate_path, source.name)
        _sync_audio_files(source_path, self.audio_output_path)
        return pd.read_csv(os.path.join(source_path, "metadata.csv"))

    def _package_data(self):
        # It syncs with existing dataset, only zipping changed files
        os.system("cd {} ; zip -qq -FSr dataset.zip dataset/".format(self.data_path))

    def compile(self) -> pd.DataFrame:
        """Compiles a dataset and returns the newly created metadata (already saved)."""
        self._prepare_output()

        dataset_metadata = pd.DataFrame()
        for source in self.sources:
            source_metadata = self._compile_source(source)
            dataset_metadata = pd.concat([dataset_metadata, source_metadata])

        clean_dataset = dataset_metadata.drop_duplicates("filename")
        diff = len(dataset_metadata) - len(clean_dataset)
        if diff != 0:
            print(f"Warning: {diff} duplicate rows found. Some rows were dropped (all files copied).")
            dataset_metadata = clean_dataset
        dataset_metadata.to_csv(self.metadata_output_path, index=False)

        self._package_data()

        return dataset_metadata