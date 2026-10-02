from flask import Blueprint, abort, redirect, url_for, render_template, request
from flask_security import current_user


base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def index():
    scenarios = []
    if current_user.is_authenticated:
        return redirect(url_for('scenario.view_scenarios'))

    return get_epa_template()
    #return render_template('base/index.html', scenarios=scenarios)


def get_epa_template():
    """
    https://www.epa.gov/web-policies-and-procedures/procedure-complying-epagov-look-and-feel
        Download uswds: https://designsystem.digital.gov/download/
            Save to /static/css/lib/uswds/
            We only need the img/ assets for just a few things, can delete the other stuff
        Download the template and move assets to /static/css/lib/uswds/epa/

    base.html
        Update <title>
        Replace `<article>` contents with `{% include 'epa/trim_login.html' %}`
        Replace Google Tag Manager code
        Update template asset paths
            ./EPA Template _ US EPA_files/
                becomes
            {{ url_for('static', filename='css/lib/uswds/epa/
        Download sprite.artifact.svg (https://www.epa.gov/themes/epa_theme/images/sprite.artifact.svg)
            Place in uswds/epa/
            Replace all the sprite.artifact.svg links e.g. 
                https://www.epa.gov/themes/epa_theme/images/sprite.artifact.svg#magnifying-glass
                    becomes
                {{ url_for('static', filename='css/lib/uswds/epa/sprite.artifact.svg')}}#magnifying-glass
        Remove references to pattern-lab (`themes/epa_theme/pattern-lab/patterns`)
        Remove optional meta data
        Keep the following scripts, remove the .download extension
            jquery.min.js
            once.min.js
            drupalSettingsLoader.js
            drupal.js
            drupal.init.js
            common.min.js
            scripts.min.js
            header-search.min.js

    uswds/epa/style.css
        Updating relative paths, see existing:
            font links (@font-face)
            images (`../images` --> `../img/`)
    """
    import re

    epa_template = render_template('epa/base.html')

    # static filepaths
    pattern = r'''\./EPA Template _ US EPA_files/([^"'?#]+)'''
    epa_template = re.sub(
        pattern,
        lambda match: url_for('static', filename=f"css/lib/uswds/epa/{match.group(1)}"),
        epa_template,
    )

    return epa_template