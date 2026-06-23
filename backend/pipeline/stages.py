from typing import Any

class PipelineStage:
    def process(self, data: Any) -> Any:
        raise NotImplementedError
