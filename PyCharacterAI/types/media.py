from datetime import datetime
from typing import Dict, Optional

from .base import BaseCAI


class Avatar(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.__image_file_name = options.get("file_name")

    def get_file_name(self) -> Optional[str]:
        return self.__image_file_name

    def get_url(self, size: int = 400, animated: bool = False) -> str:
        return (
            f"https://characterai.io/i/{size}/static/avatars/{self.get_file_name()}?"
            f"webp=true&anim={1 if animated else 0}"
        )


class Voice(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.voice_id = options.get("id")
        self.name = options.get("name", "")
        self.description = options.get("description", "")
        self.gender = options.get("gender", "neutral")

        visibility = options.get("visibility", "private")
        self.visibility = visibility.lower()

        self.preview_audio_url: Optional[str] = options.get("previewAudioURI", None)
        self.preview_text = options.get("previewText", "")

        creator_info = options.get("creatorInfo", {})
        self.creator_id: Optional[str] = creator_info.get("id", None)
        self.creator_username: Optional[str] = creator_info.get("username", None)

        self.internal_status = options.get("internalStatus", "active")

        last_update_time = options.get("lastUpdateTime", None)
        if last_update_time:
            try:
                last_update_time = datetime.strptime(str(last_update_time), "%Y-%m-%dT%H:%M:%S.%fZ")

            except ValueError:
                pass

        self.last_update_time: Optional[datetime] = last_update_time
