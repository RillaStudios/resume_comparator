COMPARE_SETTINGS = {
    "optimized": {
        "name": "Optimized",
        "description": "Optimized settings for speed. Will use the best"
                       "settings for quick performance. (Best for speed)",
    },
    "basic": {
        "name": "Basic",
        "description": "Basic settings for comparison. Will use default models,"
                       "and aim for a balance between speed and accuracy. (Best for most cases)",
    },
    "advanced": {
        "name": "Advanced",
        "description": "Advanced settings for comparison. Will use more complex models,"
                       "and aim for higher accuracy, but may be slower. (Best for accuracy)",
    },
}

from enum import Enum

class CompareSettings(Enum):
    OPTIMIZED = "optimized"
    BASIC = "basic"
    ADVANCED = "advanced"