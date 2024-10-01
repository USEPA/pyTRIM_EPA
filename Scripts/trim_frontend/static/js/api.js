
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
        var url = api.getUrl('scenario_api.copy_scenario');
        var data = makeFormData(scenario);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        })
    }

    api.deleteScenario = function(scenario) {
        var url = api.getUrl('scenario_api.delete_scenario');
        var data = makeFormData(scenario);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        })
    }

    api.getMeteorology = function(scenario) {
        var url = api.getUrl('scenario_api.get_scenario_met_data');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenario.id + '/')
        });
    }

    api.getSeasonalDynamics = function(scenario) {
        var url = api.getUrl('scenario_api.get_scenario_seasonal_dynamics');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenario.id + '/')
        });
    }

    api.getRunoffMatrix = function(scenario) {
        var url = api.getUrl('scenario_api.get_scenario_runoff_matrix');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenario.id + '/')
        });
    }

    api.getChemicals = function(scenario) {
        if (scenario === undefined) {
            var url = api.getUrl('chemicals_api.get_chemicals');
            return AJAX.call({
                url: url
            });
        }
        else {
            var url = api.getUrl('scenario_api.get_scenario_chemicals');
            return AJAX.call({
                url: url.replace('/0/', '/' + scenario.id + '/')
            });
        }
    }

    api.getParameters = function(scenario, paramNames) {
        var url = api.getUrl('scenario_api.get_parameters')
            .replace('/0/', '/' + scenario.id + '/');
        var query = [];
        for (var x of paramNames) {
            query.push('parameter=' + x)
        }
        url = url + '?' + query.join('&')
        return AJAX.call({
            url: url
        });
    }

    api.getLastResults = function(scenario) {
        var url = api.getUrl('scenario_api.get_last_results');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenario.id + '/')
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

    api.parseAERMODFile = function(fields) {
        var url = api.getUrl('file_api.parse_aermod');

        var data = makeFormData(fields);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    api.uploadParcelFile = function(fields, callbackFxn) {
        var url = api.getUrl('file_api.parse_parcel');
        var data = makeFormData(fields);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callbackFxn
        });
    };

    api.uploadSurfaceRunoffMatrixFile = function(fields, callbackFxn) {
        var url = api.getUrl('file_api.parse_runoff_matrix');
        var data = makeFormData(fields);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callbackFxn
        });
    };

    api.getSoilData = function(tillage) {
        var url = api.getUrl('external_api.get_soil_data').replace('/both', '/' + tillage);

        return AJAX.call({
            url: url
        });
    };

    api.createParcels = function(scenarioId, parcels) {
        var url = api.getUrl('parcels_api.create');
        var data = makeFormData(parcels);
        return AJAX.call({
            method: 'POST',
            url: url.replace('/0/', '/' + scenarioId + '/'),
            data: data
        });
    };

    api.getParcels = function(scenarioId) {
        var url = api.getUrl('parcels_api.get');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenarioId + '/')
        });
    };

    api.updateParcel = function(scenarioId, parcel) {
        var url = api.getUrl('parcels_api.update');
        var data = makeFormData(parcel);
        return AJAX.call({
            method: 'POST',
            url: url.replace('/0/', '/' + scenarioId + '/').replace('/-1/', '/' + data.get('id') + '/'),
            data: data
        });
    };

    api.deleteParcels = function(scenarioId, parcel) {
        var url = api.getUrl('parcels_api.delete');
        var data = makeFormData(parcel);
        parcel_id = parcel.properties.parcelid
        return AJAX.call({
            method: 'POST',
            url: url.replace('/0/', '/' + scenarioId + '/').replace('/-1/', '/' + parcel_id + '/'),
            data: data
        });
    };

    api.runModel = function(scenario_info, callback_fxn) {
        let url = api.getUrl('scenario_api.run_result_scenario');
        let data = makeFormData(scenario_info);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
			callback: callback_fxn
        });
    }

    api.clearOldResults = function(scenario_info, callback_fxn) {
        let url = api.getUrl('scenario_api.clear_old_result');
        let data = makeFormData(scenario_info);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callback_fxn
        })
    }

    api.getResults = function(scenario_info) {
        let url = api.getUrl('scenario_api.get_result_scenario');
        let data = makeFormData(scenario_info);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    }

    api.poll = function(scenario_id) {
        let url = TRIM.api.getUrl('scenario_api.poll_model_run_scenario').replace('/0', '/' + scenario_id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

    api.resetPoll = function(scenario_info) {
        let data = makeFormData(scenario_info);
        let url = api.getUrl('scenario_api.reset_poll_model_run_scenario')
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    }

    api.checkExecutionCompletion = function(execution_arn, callback_fxn) {
        let url = api.getUrl('scenario_api.check_execution_completion');
        let data = makeFormData([{ "name": "execution_arn", "value": execution_arn }])
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
			callback: callback_fxn
        });
    }

    api.fetchRunResults = function(bucket, uuid, callback_fxn) {
        let url = api.getUrl('scenario_api.fetch_run_results');
        let data = makeFormData([{ "name": "bucket", "value": bucket }, {"name": "uuid", "value": uuid}])
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
			callback: callback_fxn
        });
    }

    trim.api = api;

    trim.store = {}

    return trim;
})(window.TRIM || {});
