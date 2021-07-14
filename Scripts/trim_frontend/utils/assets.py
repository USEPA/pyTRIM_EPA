from flask_assets import Bundle


def register_site_theme(assets):
    site_theme = Bundle(
        '.dev/css/root.scss',
        depends=('css/*.scss'),
        filters='libsass,cssmin',
        output='css/theme.css',
        extra={'rel': 'stylesheet/scss'}
    )
    assets.register('site_theme', site_theme)
    site_theme.build()


def register_assets(assets):
    register_site_theme(assets)
