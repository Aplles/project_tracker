from split_settings.tools import include

settings = [
    "django.py",  # standard django settings
    "database.py",  # postgres
    "restframework.py",  # rest-framework settings
]

# Include settings:
include(*settings)
