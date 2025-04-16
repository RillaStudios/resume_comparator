COMPARE_SETTINGS = {
    "label": {
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
    },
}

from enum import Enum

class CompareSettingsType(Enum):
    OPTIMIZED = "optimized"
    BASIC = "basic"
    ADVANCED = "advanced"

class CompareSettings:

    setting: CompareSettingsType
    name: str
    description: str
    use_groq: bool

    def __init__(self, setting: CompareSettingsType, use_groq: bool = False):

        self.setting = setting
        self.name = COMPARE_SETTINGS["label"][setting.value]["name"]
        self.description = COMPARE_SETTINGS["label"][setting.value]["description"]
        self.use_groq = use_groq
