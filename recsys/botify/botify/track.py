import json
import pickle
from dataclasses import dataclass


@dataclass
class Track:
    track: int
    artist: str
    title: str


class Catalog:
    """
    A helper class used to load track data upon server startup
    and store the data to redis.
    """

    def __init__(self, app):
        self.app = app
        self.tracks = []

    def load(self, catalog_path):
        self.app.logger.info(f"Loading tracks from {catalog_path}")
        with open(catalog_path) as catalog_file:
            for j, line in enumerate(catalog_file):
                data = json.loads(line)
                self.tracks.append(Track(data["track"], data["artist"], data["title"]))
        self.app.logger.info(f"Loaded {j+1} tracks")
        return self

    def upload_tracks(self, redis):
        self.app.logger.info(f"Uploading tracks to redis")
        for track in self.tracks:
            redis.set(track.track, self.track_to_bytes(track))
        self.app.logger.info(f"Uploaded {len(self.tracks)} tracks")

    def track_to_bytes(self, track):
        return pickle.dumps(track)

    def track_from_bytes(self, bts):
        return pickle.loads(bts)
