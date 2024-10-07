from enum import Enum
'''
class NLI_LABELS(Enum):
    EXECUTE = "ejecutar"
    WH40K = "warhammer"
    CONVERSATION = "conversación"
    READ_YAHOO_MAIL = "yahoo"

'''
class NLI_LABELS(Enum):
    EXECUTE = {"label": "ejecutar", "topic": "copijidl-amanda-ia"}
    WH40K = {"label": "warhammer", "topic": "copijidl-aia-read-svc"}
    CONVERSATION = {"label": "conversación", "topic": "xxxxxx"}
    READ_YAHOO_MAIL = {"label": "yahoo", "topic": "copijidl-aia-read-svc"}

    @classmethod
    def find_enum_by_label(cls, label_value):
        for label in cls:
            if label.value["label"] == label_value:
                return label.name
        return None
    
    @classmethod
    def get_topic_by_enum_name(cls, enum_name):
        try:
            return cls[enum_name].value["topic"]
        except KeyError:
            return None