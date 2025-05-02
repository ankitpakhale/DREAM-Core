import logging


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            "DeprecationWarning",  # generic Python deprecation warnings
            "PendingDeprecationWarning",  # pending deprecation warnings
            "ResourceWarning",  # resource-related warnings (e.g., unclosed files)
        ]
        # return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])
