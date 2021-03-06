# This is a fairly standard Django settings file, with some special additions
# that allow addon applications to auto-configure themselves. If it looks 
# unfamiliar, please see our documentation:
#
#   http://docs.divio.com/en/latest/reference/configuration-settings-file.html
#
# and comments below.


# INSTALLED_ADDONS is a list of self-configuring Divio Cloud addons - see the
# Addons view in your project's dashboard. See also the addons directory in 
# this project, and the INSTALLED_ADDONS section in requirements.in.

INSTALLED_ADDONS = [
    # Important: Items listed inside the next block are auto-generated.
    # Manual changes will be overwritten.

    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-wagtail',
    # </INSTALLED_ADDONS>
]

# Now we will load auto-configured settings for addons. See:
#
#   http://docs.divio.com/en/latest/reference/configuration-aldryn-config.html
#
# for information about how this works.
#
# Note that any settings you provide before the next two lines are liable to be
# overwritten, so they should be placed *after* this section.

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

# Your own Django settings can be applied from here on. Key settings like
# INSTALLED_APPS, MIDDLEWARE and TEMPLATES are provided in the Aldryn Django
# addon. See:
#
#   http://docs.divio.com/en/latest/how-to/configure-settings.html
#
# for guidance on managing these settings.

INSTALLED_APPS.extend([
    # Extend the INSTALLED_APPS setting by listing additional applications here
    'home',
    'blog',
    'event',
    'search',
    'subscribe',
    'team',
    'site_settings',
    'gallery',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.settings',
    'captcha',
    'wagtailcaptcha',
    'wagtailmenus',
    "wagtail.contrib.routable_page",
    "shop",
    'corsheaders',
])

# To see the settings that have been applied, use the Django diffsettings 
# management command. 
# See https://docs.divio.com/en/latest/how-to/configure-settings.html#list


TEMPLATES[0]["OPTIONS"]["context_processors"].append('wagtail.contrib.settings.context_processors.settings')

MIDDLEWARE.extend([
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
        ])

CORS_ALLOWED_ORIGINS = [
    "https://konkurs.ecolabomsk.ru",
    "http://konkurs.ecolabomsk.ru",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


CSRF_COOKIE_DOMAIN = '.ecolabomsk.ru'
CSRF_TRUSTED_ORIGINS = ['.ecolabomsk.ru', 'ecolabomsk']
RECAPTCHA_PUBLIC_KEY = '6LfjnPAUAAAAAHhqKbK4IrSsPIfis1Y0YGje-gp3'
RECAPTCHA_PRIVATE_KEY = '6LfjnPAUAAAAAG0c_aoK_k02HXcR9PKNN_856ESB'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'polopolaw@gmail.com'
EMAIL_HOST_PASSWORD = 'dfuykmiqcfdzyxac'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True