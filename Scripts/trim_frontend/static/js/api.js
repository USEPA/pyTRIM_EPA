
window.TRIM = (function(trim) {
    var api = trim.api || {};

    var internalStore = trim.store || {};

    api.getScenario = function(id) {
        var url = api.getUrl('scenario_api.get_scenario').replace('/0', '/' + id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

    api.updateScenario = function(scenario) {
        var data = makeFormData(scenario);
        var id = data.get('id');
        var url = api.getUrl('scenario_api.update_scenario').replace('/0', '/' + id);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: data
        });
    };

    api.getScenarioPermissions = function(scenarioId) {
        var url = api.getUrl('scenario_api.get_permissions').replace('/0', '/' + scenarioId);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

    api.saveScenarioPermissions = function(scenarioId, newPermissions) {
        var url = api.getUrl('scenario_api.save_permissions').replace('/0', '/' + scenarioId);
        return AJAX.call({
            method: 'POST',
            url: url,
            data: {'permissions': newPermissions},
            json: true
        });
    }

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

    api.exportScenarioForMirc = function(scenario_id) {
        var url = api.getUrl('scenario_api.export_for_mirc').replace('/0', '/' + scenario_id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
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

    api.uploadBackgroundConcFile = function(fields) {
        var url = api.getUrl('file_api.upload_background_conc');

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

    api.hitUrl = function(url, callbackFxn) {
        return AJAX.call({
            method: 'GET',
            url: url,
            callback: callbackFxn
        });
	};

    api.uploadMiscScenarioFile = function(fields, callbackFxn) {
        var url = api.getUrl('file_api.manage_misc_scen_file');
        var data = makeFormData(fields);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callbackFxn
        });
    };

    api.deleteMiscScenarioFile = function(scenario_id, misc_file_type, callbackFxn) {
        var url = api.getUrl('file_api.manage_misc_scen_file');
		url += "?scenario_id=" + scenario_id + "&misc_file_type=" + misc_file_type;
        var data = makeFormData([]);

        return AJAX.call({
            method: 'DELETE',
            url: url,
            data: data,
            callback: callbackFxn
        });
    };

    api.checkMiscScenarioFile = function(scenario_id, misc_file_type, callbackFxn) {
        var url = api.getUrl('file_api.manage_misc_scen_file');
		url += "?scenario_id=" + scenario_id + "&misc_file_type=" + misc_file_type;

        return AJAX.call({
            method: 'GET',
            url: url,
            // data: data,
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

	api.checkStepFunctionStatus = function(execution_arn, callback_fxn) {
        let url = api.getUrl('general_api.stepfxn_check');
        console.log("CHECK STEPFXN STATUS URL IS: [" + url + "]");
        let data = makeFormData({type: "data", name: "arn", value: execution_arn})

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callback_fxn
        });
	}

    api.runGetFlow = function(scenario_id, callback_fxn) {
        console.log("runGetFlow (api.js)");
        let url = api.getUrl('scenario_api.run_getflow').replace("/0/", "/" + scenario_id + "/");
        console.log("RUN GETFLOW URL IS: [" + url + "]");

        let data = makeFormData([]);//scenario_info);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callback_fxn
        });
    }

    api.getLastResults = function(scenarioId) {
        var url = api.getUrl('scenario_api.get_last_results');
        return AJAX.call({
            url: url.replace('/0/', '/' + scenarioId + '/')
        });
    }

    api.clearOldResults = function(scenarioId) {
        let url = api.getUrl('scenario_api.clear_old_result');
        return AJAX.call({
            method: 'DELETE',
            url: url.replace("/0/", "/" + scenarioId + "/")
        })
    }

    api.runModel = function(scenarioId) {
        let url = api.getUrl('scenario_api.run_result_scenario');
        return AJAX.call({
            method: 'POST',
            url: url.replace('/0/', '/' + scenarioId + '/')
        });
    }

    api.refreshDebugLogs = function(scenarioId) {
        let url = api.getUrl('scenario_api.get_debug_logs');
        return AJAX.call({
            method: 'GET',
            url: url.replace('/0/', '/' + scenarioId + '/')
        });
    }

    api.runReceptorGeneration = function(scenario_id, callback_fxn) {
        let url = api.getUrl('scenario_api.run_receptor_generation').replace("/0/", "/" + scenario_id + "/");

        let data = makeFormData([]);

        return AJAX.call({
            method: 'POST',
            url: url,
            data: data,
            callback: callback_fxn
        });
    }

    api.getChemicalProperties = function(scenario_id) {
        let url = TRIM.api.getUrl('scenario_api.get_chemical_properties').replace('/0', '/' + scenario_id);
        return AJAX.call({
            method: 'GET',
            url: url
        });
    }

    api.updateParameter = (entityType, opts) => {
        if (internalStore.currentScenario == undefined) {
            throw new Error('Cannot Call `TRIM.api.updateParameter()` Before Loading a Scenario')
        }
        if (entityType === 'scenario') {
            // Update local store
            for (const field in opts) {
                if (field === 'id') {
                    continue;
                }
                internalStore.currentScenario[field] = opts[field];
            }
            // Update backend
            const postData = [
                {
                    'type': 'data',
                    'name': 'id',
                    'value': internalStore.currentScenario.id
                }
            ];
            for (const field in opts) {
                postData.push({
                    'type': 'data',
                    'name': 'field',
                    'value': field
                });
                postData.push({
                    'type': 'input',
                    'name': field,
                    'value': opts[field]
                });
            }
            return api.updateScenario(postData);
        }
        else if (entityType === 'parcel') {
            let parcelId = opts.id;
            // Update local store
            for (const pcl of internalStore.currentScenario.parcels) {
                if (pcl.id != parcelId) {
                    continue;
                }
                for (const field in opts) {
                    if (field === 'id') {
                        continue;
                    }
                    pcl[field] = opts[field];
                }
                break;
            }
            // Update backend
            const postData = [
                {
                    'type': 'data',
                    'name': 'id',
                    'value': parcelId
                }
            ];
            for (const field in opts) {
                if (field === 'id') {
                    continue;
                }
                postData.push({
                    'type': 'data',
                    'name': 'field',
                    'value': field
                });
                postData.push({
                    'type': 'input',
                    'name': field,
                    'value': opts[field]
                });
            }
            return api.updateParcel(internalStore.currentScenario.id, postData);
        }
        throw new Error('Unsupported Entity Type for `TRIM.api.updateParameter()`')
    }

    trim.api = api;
    trim.store = internalStore;

    return trim;
})(window.TRIM || {});
