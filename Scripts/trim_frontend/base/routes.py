from flask import Blueprint, redirect, url_for, render_template
from flask_security import current_user


base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def index():
    scenarios = []
    if current_user.is_authenticated:
        return redirect(url_for('scenario.view_scenarios'))

    # os.getenv('TRIM_ENV_PROFILE', 'local')
    return get_epa_template()
    #return render_template('base/index.html', scenarios=scenarios)


def get_epa_template():
    """
    WIP!

    https://www.epa.gov/web-policies-and-procedures/procedure-complying-epagov-look-and-feel
        Download the template

    base.html
        Replacing `<article>` contents with `{% include 'epa/trim_login.html' %}`
        Remove references to pattern-lab (`themes/epa_theme/pattern-lab/patterns`)
        Replace Google Tag Manager code
        Remove optional meta data
        Remove certain scripts at the bottom
            <script src="/static/epa/css.escape.js.download"></script>
            <script src="/static/epa/es6-promise.auto.min.js.download"></script>
            <script src="/static/epa/jquery.once.min.js.download"></script>
            Universal-Federated-Analytics-Min.js.download
            9240.js.download
        Replace for all sprite.artifact.svg except instagram-square I have no idea why
            https://www.epa.gov/themes/epa_theme/images/sprite.artifact.svg
                becomes
            {{url_for('static', filename='epa/uswds/img/sprite.svg')}}

    style.css
        Updating relative paths: font links (@font-face), images (`../images` --> `./uswds/img`)
    """
    import re

    epa_template = render_template('epa/base.html')

    # static filepaths
    pattern = r'''\./EPA Template _ US EPA_files/([^"'?#]+)'''
    epa_template = re.sub(
        pattern,
        lambda match: url_for('static', filename=f"epa/{match.group(1)}"),
        epa_template,
    )

    # title
    new_title = "TRIM | US EPA"
    epa_template = re.sub(
        r'(<title\b[^>]*>).*?(</title>)',
        lambda match: f"{match.group(1)}{new_title}{match.group(2)}",
        epa_template,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return epa_template