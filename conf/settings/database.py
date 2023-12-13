from conf.settings.django import env, BASE_DIR

# DATABASES = {"default": env.db()}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
