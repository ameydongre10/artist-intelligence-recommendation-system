"""
Safe Dataset Loader.
Consumes the verified dataset_inventory.json map without hardcoded assumptions
and provides typed, safe access to artist records, media files, and hirer briefs.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from src.utils.file_utils import read_json_file, resolve_path
from src.utils.errors import FileNotFoundCustomError, ProcessingFailedError
from src.models.common import ArtistCategory


class DatasetLoader:
    """
    Safe loader accessing the verified raw dataset through dataset_inventory.json.
    """
    def __init__(self, inventory_path: str = "data/processed/dataset_inventory.json", raw_base_dir: str = "data/raw"):
        self.inventory_path = inventory_path
        self.raw_base_dir = raw_base_dir
        self._inventory: Optional[Dict[str, Any]] = None

    def load_inventory(self) -> Dict[str, Any]:
        """Loads and caches the dataset inventory dictionary."""
        if self._inventory is None:
            path = resolve_path(self.inventory_path)
            if not path.exists():
                raise FileNotFoundCustomError(
                    str(path),
                    details={"hint": "Run scripts/inventory_dataset.py to generate dataset_inventory.json"}
                )
            self._inventory = read_json_file(str(path))
        return self._inventory

    def get_metadata(self) -> Dict[str, Any]:
        """Returns the dataset metadata."""
        inv = self.load_inventory()
        return inv.get("dataset_metadata", {})

    def get_hirer_conversations(self) -> List[Dict[str, Any]]:
        """Returns all 4 hirer conversation records."""
        inv = self.load_inventory()
        return inv.get("hirer_conversations", [])

    def get_hirer_conversation_by_id(self, brief_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific hirer conversation by brief_id."""
        for conv in self.get_hirer_conversations():
            if conv["brief_id"] == brief_id or conv["filename"].startswith(brief_id):
                return conv
        return None

    def get_follow_up_updates(self) -> List[Dict[str, Any]]:
        """Returns all follow-up updates."""
        inv = self.load_inventory()
        return inv.get("follow_up_updates", [])

    def get_follow_up_by_id(self, update_id: str = "01_cafe_music_update") -> Optional[Dict[str, Any]]:
        """Retrieve a specific follow-up update by update_id."""
        for fu in self.get_follow_up_updates():
            if fu["update_id"] == update_id or fu["filename"].startswith(update_id):
                return fu
        return None

    def get_all_artists(self, category: Optional[ArtistCategory] = None) -> List[Dict[str, Any]]:
        """
        Returns all artist records across all categories (or filtered by category).
        """
        inv = self.load_inventory()
        artists_dict = inv.get("artist_profiles", {})
        
        cats_to_fetch = []
        if category:
            cat_key = f"{category.value}s" if not category.value.endswith("s") else category.value
            cats_to_fetch = [cat_key]
        else:
            cats_to_fetch = ["photographers", "musicians", "video_editors"]

        result = []
        for cat in cats_to_fetch:
            result.extend(artists_dict.get(cat, []))
        return result

    def get_artist_by_identifier(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an artist record by source_folder_name, folder_inferred_id, or profile_declared_id.
        """
        id_clean = identifier.strip().upper()
        for artist in self.get_all_artists():
            folder_name = artist["source_folder_name"].upper()
            folder_id = artist["folder_inferred_id"].upper()
            profile_id = (artist["profile_declared_id"] or "").upper()
            
            if id_clean == folder_name or id_clean == folder_id or (profile_id and id_clean == profile_id):
                return artist
        return None

    def get_artist_media_paths(self, identifier: str) -> List[str]:
        """Returns the list of relative file paths for all media files of an artist."""
        artist = self.get_artist_by_identifier(identifier)
        if not artist:
            return []
        return [m["relative_path"] for m in artist["media_summary"]["media_files"]]

    def get_anomalies(self) -> List[Dict[str, Any]]:
        """Returns all documented dataset anomalies."""
        inv = self.load_inventory()
        return inv.get("dataset_anomalies", [])
