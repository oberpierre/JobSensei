from enum import Enum

class Topic(Enum):
    START = 'jobsensei-sourcing-start-v1'
    END = 'jobsensei-sourcing-end-v1'
    SOURCING = 'jobsensei-sourcing-v1'
    NEW = 'jobsensei-sourcing-new-v1'
    DELETE = 'jobsensei-sourcing-delete-v1'