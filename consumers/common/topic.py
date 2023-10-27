from enum import Enum

class Topic(Enum):
    SRC_START = 'jobsensei-sourcing-start-v1'
    SRC_END = 'jobsensei-sourcing-end-v1'
    SRC_SOURCING = 'jobsensei-sourcing-v1'
    SRC_NEW = 'jobsensei-sourcing-new-v1'
    SRC_DELETE = 'jobsensei-sourcing-delete-v1'
    SRC_CATEGORIZED = 'jobsensei-sourcing-categorized-v1'
    LLM_CATEGORIZE = 'jobsensei-llm-categorize-v1'