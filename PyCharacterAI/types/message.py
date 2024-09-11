from datetime import datetime
from typing import Union, Dict

from .base import BaseCAI


# Chat v1
class HistoryMessage(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.uuid = options.get("uuid")
        self.id = options.get("id")
        self.text = options.get("text", "")
        self.src = options.get("src")
        self.tgt = options.get("tgt")
        self.is_alternative = options.get("is_alternative")
        self.image_relative_path = options.get("image_rel_path", "")


# Chat v2
class TurnCandidate(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)

        self.candidate_id = options.get("candidate_id")
        self.text = options.get("raw_content", "")
        self.is_final = options.get("is_final", False)
        self.is_filtered = options.get("safety_truncated", False)

        create_time = options.get("create_time")

        if create_time:
            try:
                create_time = datetime.strptime(str(create_time), "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                pass

        self.create_time: Union[datetime, None] = create_time


class Turn(BaseCAI):
    def __init__(self, options: Dict):
        super().__init__(options)
        turn_key = options.get("turn_key")
        
        self.chat_id = turn_key.get("chat_id")
        self.turn_id = turn_key.get("turn_id")

        create_time = options.get("create_time", None)

        if create_time:
            try:
                create_time = datetime.strptime(str(create_time), "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                pass

        self.create_time: Union[datetime, None] = create_time

        last_update_time = options.get("last_update_time", None)

        if last_update_time:
            try:
                last_update_time = datetime.strptime(str(last_update_time), "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                pass

        self.last_update_time: Union[datetime, None] = last_update_time

        self.state = options.get("state")
        
        author = options.get("author", {})
        self.author_id = author.get("author_id", "")
        self.author_name = author.get("name", "")
        self.author_is_human = author.get("is_human", False)

        self.candidates: {str: TurnCandidate} = {}

        for raw_candidate in options.get("candidates", []):
            candidate = TurnCandidate(raw_candidate)

            self.candidates[candidate.candidate_id] = candidate

        self.primary_candidate_id: Union[str, None] = options.get("primary_candidate_id", None)

    def get_candidates(self) -> [TurnCandidate]:
        return self.candidates.values()

    def get_primary_candidate(self) -> Union[TurnCandidate, None]:
        return self.candidates.get(self.primary_candidate_id, None)
