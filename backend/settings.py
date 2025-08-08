INSTALLED_APPS = [
    ...
    'collectors',
]

ALLOWED_HOSTS = [
    'findocscollector.onrender.com',
    'fin-docs-collector.vercel.app',
    'localhost',
    '127.0.0.1'
]

CORS_ALLOWED_ORIGINS = [
    'https://fin-docs-collector.vercel.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://fin-docs-collector.vercel.app',
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'backend', 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
