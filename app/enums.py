from enum import Enum

class JobStatus(Enum):
    PENDING = 'pending'
    APPLIED = 'applied'
    INTERVIEW = 'interview'
    REJECTED = 'rejected'