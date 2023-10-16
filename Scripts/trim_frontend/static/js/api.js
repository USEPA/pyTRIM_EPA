
window.TRIM = (function(trim) {
    var api = trim.api || {};

    api.getScenario = function(id) {
        var url = api.getUrl('scenario_api.get_scenario').replace('/0', '/' + id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

     api.updateScenario = function(scenario) {
        var url = api.getUrl('scenario_api.update_scenario');
        var data = makeFormData(scenario);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    api.copyScenario = function(scenario) {
        var url = api.getUrl('secnario_api.copy_scenario');
        var data = makeFormData(scenario);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        })
    }

    api.deleteScenario = function(scenario) {
        var url = api.getUrl('secnario_api.delete_scenario');
        var data = makeFormData(scenario);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        })
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
            else if (field.type === 'Feature') {
                let GIS_data = field.properties
                GIS_data.geom = field.geometry.coordinates[0]
                for (var key in GIS_data) {
                    formData.append(key, (key === 'geom') ? JSON.stringify(GIS_data[key]) : GIS_data[key])
                }
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

    api.getSoilData = function(tillage) {
        var url = api.getUrl('external_api.get_soil_data').replace('/both', '/' + tillage);

        return AJAX.call({
            url: url
        });
    };

    api.createParcels = function(parcels) {
        var url = api.getUrl('parcels_api.create');
        var data = makeFormData(parcels);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    api.getParcels = function() {
        var url = api.getUrl('parcels_api.get');
        return AJAX.call({
            url: url
        });
    };

    api.updateParcel = function(parcel) {
        var url = api.getUrl('parcels_api.update');
        var data = makeFormData(parcel);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    api.deleteParcels = function(parcels) {
        var url = api.getUrl('parcels_api.delete');
        var data = makeFormData(parcels);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    trim.api = api;
    return trim;
})(window.TRIM || {});
