
window.TRIM = (function(trim) {
    var api = trim.api || {};

    api.getScenario = function(id) {
        var url = api.getUrl('scenario_api.get_scenario').replace('/0', '/' + id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

    api.loadForms = function(names) {
        if (!names) {
            return undefined;
        }
        if (!Array.isArray(names)) {
            names = [names];
        }
        names = names.slice(0); // clone array

        var url = api.getUrl('file_api.load_json_form');

        url += '?'
        var params = []
        while (names.length) {
            var form = names.pop();
            params.push('form=' + form);
        }
        url += params.join('&');

        return AJAX.call({
            method: 'GET',
            url: url
        });
    };

    function makeFormData(fields) {
        if (!Array.isArray(fields)) {
            fields = [fields];
        }

        var form = document.createElement('form');
        form.setAttribute('enctype', 'multipart/form-data');
        var formData = new FormData(form);

        for (var i = 0, len = fields.length; i < len; i++) {
            var field = fields[i];

            if (field.type === 'file') {
                formData.append(field.name, field.files[0])
            }
            else {
                formData.append(field.name, field.value)
            }
        }

        if (formData.get('csrf_token') == null) {
            formData.append('csrf_token', api.getCSRF());
        }

        return formData;
    }

    api.parseFiles = function(fields) {
        var url = api.getUrl('file_api.parse');

        var data = makeFormData(fields);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    trim.api = api;
    return trim;
})(window.TRIM || {});
