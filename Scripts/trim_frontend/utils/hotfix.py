import wtforms_sqlalchemy.fields as f
from wtforms.fields import Field
from trim_db.schema.utils.caching import CacheManager


def patch_wtforms_sqlalchemy():
    """Fixes https://github.com/wtforms/wtforms-sqlalchemy/issues/9
    """
    def get_pk_from_identity(obj):
        cls, key = f.identity_key(instance=obj)[:2]
        return ':'.join(f.text_type(x) for x in key)

    f.get_pk_from_identity = get_pk_from_identity


def add_help_text_to_forms():
    """This allows us to have both collapsible help-text
    for form fields, as well as always-visible description
    text if desired.
    """
    Field.help_text = ""
    old_init = Field.__init__

    def new_init(s, *args, help_text="", **kwargs):
        old_init(s, *args, **kwargs)
        s.help_text = help_text

    Field.__init__ = new_init


def patch_flask(app):
    patch_wtforms_sqlalchemy()
    add_help_text_to_forms()

    @app.before_request
    def clear_old_cache():
        CacheManager.clear_all()
