window.TRIM = (function (trim) {
    var leaflet = trim.leaflet || {};

    leaflet.map = undefined;
    leaflet.parcels = undefined;
    leaflet.requires_reload = false;

    const parcelsTableRedrawEvent = new Event('parcels:tableRedraw');

    // dot is the leaflet internal id
    // parcel is object containing the TRIM parcel id and the leaflet internal id
    // e.g.:
    // { leafletDotIdOne: { trimParcelId: A, leafletPolygonId: B }, leafletDotIdTwo: { trimParcelId: foo, leafletPolygonId: bar } }
    var dotToParcel = {};

    // These are set in initLayers
    var depositionOverlayGroup,
        receptorOverlayGroup,
        mapLayers,
        measurementControl;

    var receptorOverlayShowing = false;
    var quartileGradient = ["#D8C56C", "#C55B6C", "#A03C8E", "#7D1F4B"]; // low->high
    var conditionalSnapSettings = {
        "vertices": true,
        "segments": false
    };

    leaflet.initServices = function () {
        let services = [
            leaflet.initLayers,
            leaflet.initSmartSnap,
            leaflet.initGeojsonDownload,
            leaflet.initGeojsonUpload,
            leaflet.initDepositionOverlay,
            leaflet.initAermodReceptors,
            leaflet.initHtmlAdjustments,
        ]

        for (let service of services) {
            try { service(); } catch (e) { console.error(`${service}`, e); }
        }
    }

    leaflet.initHtmlAdjustments = function () {
        // make measuring and use of other tools mutually exclusive
        $("a.leaflet-control-draw-measure").click((e) => {
            if ($(e.target).parent().hasClass("enabled")) {
                leaflet.map.pm.disableDraw();
                leaflet.map.pm.disableGlobalEditMode();
                leaflet.map.pm.disableGlobalRemovalMode();
                leaflet.map.pm.Toolbar.buttons.removalMode.disable();
                leaflet.map.pm.Toolbar.buttons.editMode.disable();
                leaflet.map.pm.Toolbar.buttons.drawPolygon.disable();
            } else {
                leaflet.map.pm.Toolbar.buttons.removalMode.enable();
                leaflet.map.pm.Toolbar.buttons.editMode.enable();
                leaflet.map.pm.Toolbar.buttons.drawPolygon.enable();
            }
        });

        // Leaflet button 508c
        $("a.leaflet-control-zoom-in, a.leaflet-control-zoom-out").attr("tabindex", "0");
        $("a[class^='leaflet']").attr("aria-label", "Leaflet map button");
    }

    // parcel interactions -- START
    // see https://geoman.io/docs/leaflet/modes/edit-mode
    leaflet.initParcelLayer = function () {
        return L.layerGroup();
    }

    // reconstruct parcels based on map
    leaflet.refreshParcels = function () {
        function createParcel(parcel) {
            let new_parcel = new L.polygon(parcel.data.vertices.map(e => [e[1], e[0]]))
            let feature = new_parcel.feature = new_parcel.feature || {};
            feature.type = "Feature";
            feature.properties = feature.properties || {};
            new_parcel.feature.properties.parcelid = parcel.data.id;
            new_parcel.feature.properties.name = parcel.data.name;
            new_parcel.feature.properties.desc = parcel.data.description;
            new_parcel.feature.properties.area = parcel.data.area;
            new_parcel.feature.properties.air = parcel.data.hasAir;
            new_parcel.feature.properties.parceltype = parcel.data.parcelType
            new_parcel.feature.properties.receptor_spacing = parcel.data.receptor_spacing;
            new_parcel.feature.properties.landuse = { 'lu': parcel.data.landUse, 'list': parcel.media };
            new_parcel.feature.properties.farmfoodchain = parcel.data.hasFarmFoodChain;
            new_parcel.feature.properties.fishfoodweb = parcel.data.hasFishFoodWeb;
            new_parcel.feature.properties.wetland = parcel.data.hasWetland;
            parcels.addLayer(new_parcel);
        }

        let scenarioParcels = TRIM.store.currentScenario.parcels,
            standardMedia = TRIM.store.currentScenario.standardMedia,
            parcels = leaflet.initParcelLayer();

        scenarioParcels.forEach(function (e, i) {
            let this_parcel_data = { 'data': e, 'media': standardMedia }
            createParcel(this_parcel_data)
        });

        leaflet.parcels = parcels
        return parcels;
    }

    leaflet.drawParcels = function () {
        function plotSavedParcels() {
            leaflet.focusMap();
            for (const layer of Object.values(leaflet.parcels._layers)) {
                layer.addTo(leaflet.map);
                layer.bindTooltip(layer.feature.properties.name, { permanent: false }).addTo(leaflet.map);
            }
        }

        leaflet.refreshParcels();
        leaflet.map.whenReady(plotSavedParcels);
        setTimeout(function () { leaflet.refreshMap() }, 1000);
    }

    leaflet.addParcel = function (layer) {
        function validateParcelName(sName) {
            let parcelList = TRIM.store.currentScenario.parcels;
            let invalid_starts = [
                "air",
                "sw",
                "sed",
                "surfsoil",
                "rootsoil",
                "vadosesoil",
                "gw"
            ];
            for (let substr of invalid_starts) {
                if (sName.toLowerCase().startsWith(substr)) {
                    alert(`Invalid start. Parcel name cannot start with any of the following words: ${invalid_starts}`);
                    return false;
                }
            }
            if (sName.indexOf(' ') >= 0) {
                alert(`Parcel name can't contain spaces`);
                return false;
            }
            else if (parcelList.filter(p => p.name.toLowerCase() == sName.toLowerCase()).length > 0) {
                alert(`Parcel name already exists`);
                return false;
            }
            return true;
        }

        function saveIdIW(event) {
            let parcel = event.data.parcel;
            var sName = $('#shapeName').val();
            var sDesc = $('#shapeDesc').val();
            var Area = L.GeometryUtil.geodesicArea(parcel.getLatLngs()[0]);
            var sArea = Area.toString();

            if (!validateParcelName(sName)) {
                return;
            }

            parcel.feature.properties.name = sName;
            parcel.feature.properties.desc = sDesc;
            parcel.feature.properties.area = sArea;
            parcel.feature.properties.parceltype = "Land & Air"
            parcel.feature.properties.air = "No";
            parcel.feature.properties.landuse = "Nozq   "; // we will need NLCD data here?
            parcel.feature.properties.farmfoodchain = "No";
            parcel.feature.properties.fishfoodweb = "No";
            parcel.feature.properties.wetland = "No";
            leaflet.map.closePopup();
            leaflet.parcels.addLayer(parcel);

            LoadingScreen.show('create_parcel');
            TRIM.api.createParcels(TRIM.store.currentScenario.id, parcel.toGeoJSON()).on('load', function () {
                let resp = JSON.parse(this.responseText)
                if (resp) {
                    let new_parcel = resp['parcel']
                    parcel.feature.properties.parcelid = new_parcel["id"]
                    parcel.feature.properties.area = new_parcel["area"]
                    parcel.feature.properties.air = new_parcel["hasAir"]
                    parcel.feature.properties.parceltype = new_parcel["parcelType"]
                    parcel.feature.properties.landuse = { 'lu': new_parcel["landUse"], 'list': resp.media }
                    parcel.feature.properties.farmfoodchain = new_parcel["hasFarmFoodChain"]
                    parcel.feature.properties.fishfoodweb = new_parcel["hasFishFoodWeb"]
                    parcel.feature.properties.wetland = new_parcel["hasWetland"]
                    parcel.feature.properties.wetland = new_parcel["hasWetland"]
                    parcel.feature.properties.receptor_spacing = new_parcel["receptor_spacing"];

                    leaflet.parcels.addLayer(parcel);
                    parcel.bindTooltip(parcel.feature.properties.name, { permanent: false }).addTo(leaflet.map);

                    if (TRIM.store.currentScenario.parcels.length > 0) {
                        TRIM.store.currentScenario.parcels.push(new_parcel);
                    }
                }
                leaflet.refreshParcels();
                leaflet.focusMap();
                document.body.dispatchEvent(parcelsTableRedrawEvent);
                leaflet.requires_reload = true;
                LoadingScreen.hide('create_parcel');
            })
        };

        // Map and Parcel Table Functions
        var idIW = L.popup();
        parcel = layer;
        var feature = parcel.feature = parcel.feature || {};
        feature.type = "Feature";
        feature.properties = feature.properties || {};
        let parcelDrawHelpText = "Enter an arbitrary but unique name for the parcel. Names should not begin with Air, SW, Sed, SurfSoil, RootSoil, VadoseSoil, or GW. Names should not contain spaces. We recommend short names (e.g., less than about 15 characters) because they will be displayed on other pages of this user interface.<br/><br/>Also enter an arbitrary description of the parcel. It will not be used within the modeling.";
        var content = '<span>' + parcelDrawHelpText + '<br/><br/><b>Parcel Name</b></span><br/><input id="shapeName" type="text"/><br/><br/><span><b>Parcel Description<b/></span><br/><textarea id="shapeDesc" cols="25" rows="5"></textarea><br/><br/><input type="button" id="okBtn" value="Save"/>';
        idIW.setContent(content);
        idIW.setLatLng(layer.getBounds().getCenter());
        idIW.openOn(leaflet.map);
        $('#okBtn').on('click', null, { parcel: parcel }, saveIdIW)
    }

    leaflet.removeParcel = function (layer) {
        LoadingScreen.show('delete_parcel');
        let parcelObj = layer.toGeoJSON();
        parcelObj.properties.parcelid = getParcelByKey('name', parcelObj.properties.name)?.id
        TRIM.api.deleteParcels(TRIM.store.currentScenario.id, parcelObj).on('load', function () {
            // delete parcel from TRIM.store
            const idx = TRIM.store.currentScenario.parcels.findIndex(p => p.id == parcelObj.properties.parcelid);
            if (idx > -1) {
                TRIM.store.currentScenario.parcels.splice(idx, 1);
            }
            leaflet.requires_reload = true;
            leaflet.refreshParcels();
            leaflet.focusMap();
            document.body.dispatchEvent(parcelsTableRedrawEvent);
            LoadingScreen.hide('delete_parcel');
        });
    }
    // parcel interactions -- END

    // leaflet functionality -- START
    leaflet.initMap = function (mapId) {
        var map = L.map(mapId, { drawControl: false }).setView([35.99, -78.90], 12);

        let clearParcelAssociations = function (parcelId) {
            for (let dotId in dotToParcel) {
                if (dotToParcel[dotId] == parcelId) {
                    delete dotToParcel[dotId];
                }
            }
        };

        map.on('layerremove', function (e) {
            if (e.layer.feature !== undefined) { // a parcel polygon was just deleted by the user...
                clearParcelAssociations(e.layer.feature.properties.parcelid);

                let relatedStampId = L.stamp(e.layer);
                map.eachLayer(function (probe) {
                    if (probe.dotMarkerData !== undefined &&
                        probe.dotMarkerData.type == "VertexDotMarkers" &&
                        (probe.dotMarkerData.properties.relatedParcelId == e.layer.feature.properties.parcelid ||
                            probe.dotMarkerData.properties.relatedLeafletId == relatedStampId)) {
                        map.removeLayer(probe);
                        return;
                    }
                });
            } else {
                let deletedId = L.stamp(e.layer);
                if (deletedId in dotToParcel) {
                    // user clicked on an individual dot making up a parcel, not the middle of the parcel...let's delete the
                    // underlying parcel...
                    map.eachLayer(function (probe) {
                        if (probe.feature !== undefined &&
                            probe.feature.type == "Feature" &&
                            (probe.feature.properties.parcelid == dotToParcel[deletedId].trimParcelId ||
                                L.stamp(probe) == dotToParcel[deletedId].leafletPolygonId)) {
                            map.removeLayer(probe);
                            leaflet.removeParcel(probe);
                            return;
                        }
                    });
                }
            }
        });

        // START -- dots on vertices
        let addParcelAssociation = function (elementId, storageStructure, storageKey, associationType) {
            if (associationType === undefined) {
                associationType = "oneToOne";
            }

            if (associationType == "oneToMany") {
                if (!(storageKey in storageStructure)) {
                    storageStructure[storageKey] = [];
                }
                if (!(elementId in storageStructure[storageKey])) {
                    storageStructure[storageKey].push(elementId);
                }
            } else if (associationType == "oneToOne") {
                storageStructure[storageKey] = elementId;
            }
        };


        let mapDotColor = "#3388ff";

        // EDIT MODE - start
        let globalEditMode = false;
        let globalEditBuildup = {}; // dictionary of { parcel_id: lat_lng_array }
        map.on('pm:globaleditmodetoggled', function (e) {
            globalEditMode = e.enabled;

            if (globalEditMode) {
                // console.log("EDITME handle prep...");
                globalEditBuildup = {};
            } else if (!globalEditMode) {
                // console.log("EDITME handle cleanup/update...");

                let numParcelsToUpdate = 0;
                for (let key in globalEditBuildup) {
                    numParcelsToUpdate++;
                }

                let finishedCounter = 0;
                for (let key in globalEditBuildup) {
                    let coords = globalEditBuildup[key];
                    console.log("SAVE: " + coords + " for parcel " + key);
                    let parcel_info = [{
                        'type': 'data',
                        'name': 'id',
                        'value': key
                    }, {
                        'type': 'data',
                        'name': 'field',
                        'value': 'vertices'
                    }, {
                        'type': 'input',
                        'name': 'vertices',
                        'value': JSON.stringify(coords)
                    }]

                    TRIM.api.updateParcel(TRIM.store.currentScenario.id, parcel_info).on('load', function () {
                        finishedCounter++;
                        // console.log("finished [" + finishedCounter + "/" + numParcelsToUpdate + "]");
                        if (finishedCounter >= numParcelsToUpdate) {
                            window.location.reload(); // reload the page; redraws the dotMarkers, etc.
                        }
                    });
                    // FUTURE ENHANCEMENT - do we want to try to be smart if moving a shared vertex?
                    // e.g. if vertex is in two parcels we could try to update it for both...
                }
                globalEditBuildup = {};
            }
        });
        // EDIT MODE - end

        // as soon as a vertex change is made, we are going to reload the page at the end.
        // easiest way to handle the blue dotMarkers is to just remove them all at this point.
        // the page reload will re-add them at the new vertex locations.
        //
        // alternative would be to constantly be moving vertices around but that doesn't really seem
        // worth the trouble.
        let hideAllDotMarkers = function () {
            map.eachLayer(function (probe) {
                if (probe.dotMarkerData !== undefined && probe.dotMarkerData.type == "VertexDotMarkers") {
                    let dots = probe.getLayers();
                    for (let i = 0; i < dots.length; i++) {
                        let dot = dots[i];
                        dot.setStyle({ opacity: 0, fillOpacity: 0 });
                    }
                }
            });
        };

        // case 1 -- fires on initial load, NOT when drawing a parcel on-the-fly
        map.on('layeradd', function (e) {
            // user is editing vertices...
            let vertexChangesMade = false;
            e.layer.on('pm:change', function (e) {
                if (globalEditMode === true) {
                    let parcelName = e.layer.feature.properties.name;
                    let parcelId = e.layer.feature.properties.parcelid;
                    let coords = e.latlngs[0];
                    // console.log("EDITME: '" + parcelName + "' (" + parcelId + ") resize, now has " + coords.length + " points");
                    let rawLatLongs = [];
                    for (let i = 0; i < coords.length; i++) {
                        rawLatLongs.push([coords[i].lat, coords[i].lng]);
                    }
                    rawLatLongs.push([coords[0].lat, coords[0].lng]); // add trailing vertex to close
                    globalEditBuildup[parcelId] = rawLatLongs;
                }

                // fire the very first time a user moves a vertex, just one time.
                for (let key in globalEditBuildup) {
                    if (!vertexChangesMade) {
                        vertexChangesMade = true;
                        hideAllDotMarkers();
                        break;
                    }
                }
            });


            if (e.layer.feature === undefined) {
                return; // a parcel polygon was just added...doesn't fire for e.g. dotMarkers
            }

            let parcelDefinition = TRIM.store.currentScenario.parcels.find((element) => element.id == e.layer.feature.properties.parcelid);
            if (parcelDefinition === undefined) {
                return;
            }
            let dotMarkers = [];
            for (let i = 0; i < parcelDefinition.vertices.length - 1; i++) {
                let vertex = parcelDefinition.vertices[i];
                // reverse lat/long; leaflet expects different order than we use in TRIM
                let dotMarker = L.circleMarker([vertex[1], vertex[0]], { radius: 3, stroke: true, color: mapDotColor });
                dotMarkers.push(dotMarker);

                // note that these dots are currently "behind" the lines; that's ok since they're the same color.
                // If we wanted a different color, look into:
                // https://gis.stackexchange.com/questions/137061/changing-layer-order-in-leaflet
                // basically we could call bringToFront on each marker - not doing it as long as colors are same.

                addParcelAssociation({ // tracking for deletions
                    "trimParcelId": e.layer.feature.properties.parcelid,
                    "leafletPolygonId": L.stamp(e.layer)
                }, dotToParcel, L.stamp(dotMarker));
            }

            // We need to be able to delete this group when the underlying parcel is deleted, otherwise we'll
            // have some random dots still left on the map.
            // could either store "lg" somewhere to access later...
            // ...or we can just put some data onto the leaflet object in relatedParcelId, and look it up during a delete.
            // that's what we'll do.
            let lg = L.layerGroup(dotMarkers).addTo(map);
            let dotMarkerData = lg.dotMarkerData = lg.dotMarkerData || {};
            dotMarkerData.type = "VertexDotMarkers";
            dotMarkerData.properties = dotMarkerData.properties || {};
            lg.dotMarkerData.properties.relatedParcelId = e.layer.feature.properties.parcelid;
            lg.dotMarkerData.properties.relatedLeafletId = L.stamp(e.layer);
        });

        // case 2 -- fires when drawing a parcel on-the-fly. We don't have an entry in currentScenario.parcels so all we can use is
        // the internal leaflet id we get by calling L.stamp
        map.on('pm:create', ({ layer }) => {
            let dotMarkers = [];
            for (let i = 0; i < layer._latlngs[0].length; i++) {
                let dotMarker = L.circleMarker(layer._latlngs[0][i], { radius: 3, stroke: true, color: mapDotColor });
                dotMarkers.push(dotMarker);

                // track here as well
                addParcelAssociation({
                    "trimParcelId": null,
                    "leafletPolygonId": L.stamp(layer)
                }, dotToParcel, L.stamp(dotMarker));
            }

            let lg = L.layerGroup(dotMarkers).addTo(map);

            let dotMarkerData = lg.dotMarkerData = lg.dotMarkerData || {};
            dotMarkerData.type = "VertexDotMarkers";
            dotMarkerData.properties = dotMarkerData.properties || {};
            lg.dotMarkerData.properties.relatedParcelId = null; // no entry in currentScenario.parcels...
            lg.dotMarkerData.properties.relatedLeafletId = L.stamp(layer);
            leaflet.refreshParcels()
        });
        // FINISH -- dots on vertices

        // add parcel
        map.on('pm:create', ({ layer }) => {
            map.pm.setGlobalOptions({ snapSegment: leaflet.getSmartSnapSetting("segments") });
            leaflet.addParcel(layer);
        });

        // delete parcel
        map.on('pm:remove', ({ layer }) => {
            leaflet.map.removeLayer(layer);
            leaflet.removeParcel(layer);
        });

        leaflet.map = map;
        return map;
    }

    leaflet.refreshMap = function () {
        leaflet.map.invalidateSize();
    }

    leaflet.focusMap = function () {
        let scenarioParcels = TRIM.store.currentScenario.parcels;
        if (scenarioParcels.length == 0) {
            return;
        }
        let lat_means = []
        let lon_means = []
        scenarioParcels.forEach(function (e, i) {
            lon_means.push(e.vertices.map((c, i, arr) => c[0] / arr.length).reduce((p, c) => c + p))
            lat_means.push(e.vertices.map((c, i, arr) => c[1] / arr.length).reduce((p, c) => c + p))
        })
        let mean_lat = lat_means.map((c, i, arr) => c / arr.length).reduce((p, c) => c + p)
        let mean_lon = lon_means.map((c, i, arr) => c / arr.length).reduce((p, c) => c + p)
        leaflet.map.setView([mean_lat, mean_lon], 12);
    }

    leaflet.initLayers = function () {
        var StreetBM = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2JiaXJ5b2wiLCJhIjoiY2xnZHZ4cnVvMGcwZTNkcXJ6ZTNvM3N0dSJ9.S6TzhpcjiSv1qttl8B1UMA', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1
        }).addTo(leaflet.map);

        var Esri_WorldTopoMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
        });

        var Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        });

        var wmsNLCD2016 = L.tileLayer.wms('https://www.mrlc.gov/geoserver/mrlc_display/NLCD_2016_Land_Cover_L48/ows?SERVICE=WMS&', {
            layers: 'NLCD_2016_Land_Cover_L48'
        });

        var wmsFlowLine = L.tileLayer.wms('https://hydro.nationalmap.gov/arcgis/services/NHDPlus_HR/MapServer/WMSServer?', {
            layers: "7",
            transparent: true,
            format: 'image/png'
        });

        var wmsHUC12 = L.tileLayer.wms('https://hydro.nationalmap.gov:443/arcgis/services/NHDPlus_HR/MapServer/WmsServer?', {
            layers: "0",
            transparent: true,
            format: 'image/png'
        });

        var wmsLakes = L.tileLayer.wms('https://hydro.nationalmap.gov:443/arcgis/services/NHDPlus_HR/MapServer/WmsServer?', {
            layers: "3",
            transparent: true,
            format: 'image/png'
        });

        var togglelayers = L.layerGroup([wmsNLCD2016])
        var overlayMaps = {
            "NLCD": togglelayers,
            "Flowline - Large Scale": wmsFlowLine,
            "HUC12 Boundaries": wmsHUC12,
            // "Deposition": depositionOverlayGroup
        }
        var baseMaps = {
            "Streets Basemap": StreetBM,
            "Topography": Esri_WorldTopoMap,
            "Imagery": Esri_WorldImagery,
        }
        depositionOverlayGroup = L.layerGroup();
        receptorOverlayGroup = null;
        mapLayers = L.control.layers(baseMaps, overlayMaps).addTo(leaflet.map);

        leaflet.map.pm.addControls({
            position: 'topleft',
            drawMarker: false,
            drawPolyline: false,
            drawCircle: false,
            drawCircleMarker: false,
            drawRectangle: false,
            dragMode: false,
            cutPolygon: false,
            rotateMode: false,
            editMode: true,
        });

        measurementControl = L.Control.measureControl().addTo(leaflet.map);
    }
    // leaflet functionality -- END

    // additional leaflet buttons -- START
    leaflet.getSmartSnapSetting = function (typeOfSnap) {
        if (typeOfSnap == "vertices" || typeOfSnap == "segments") {
            return conditionalSnapSettings[typeOfSnap];
        } else {
            console.log("getSmartSnapSetting doesn't work with '" + typeOfSnap + "'");
        }
    };

    leaflet.smartSnapToggle = function (typeOfSnap, enableOrDisable) {
        if (typeOfSnap == "vertices" || typeOfSnap == "segments") {
            conditionalSnapSettings[typeOfSnap] = enableOrDisable;

            if (typeOfSnap == "vertices") {
                leaflet.map.pm.setGlobalOptions({ snapVertex: enableOrDisable });
            } else if (typeOfSnap == "segments") {
                leaflet.map.pm.setGlobalOptions({ snapSegment: enableOrDisable });
            }

            let bothSnapsDisabled = conditionalSnapSettings["vertices"] == false && conditionalSnapSettings["segments"] == false;
            leaflet.map.pm.setGlobalOptions({ snappable: !bothSnapsDisabled });
        } else {
            console.log("smartSnapEnableOrDisable doesn't work with '" + typeOfSnap + "'");
        }
    };

    leaflet.initSmartSnap = function () {
        let customSnapControls = [
            { "name": "ToggleSnapToVertices", "thing": "vertices" },
            { "name": "ToggleSnapToSegments", "thing": "segments" },
        ];

        for (let i = 0; i < customSnapControls.length; i++) {
            let snapThing = customSnapControls[i].thing;
            leaflet.map.pm.Toolbar.createCustomControl({
                name: customSnapControls[i].name,
                block: "custom", // draw,edit,custom,options
                title: "Snap to " + snapThing,
                onClick: function (evt, btn) { leaflet.smartSnapToggle(snapThing, !this.toggleStatus); },
                disableOtherButtons: false, disableByOtherButtons: false,
                className: "trim-custom-icon-" + snapThing,
            });

            // I can't find a way to programmatically select these, so do it with jquery...
            if (conditionalSnapSettings[snapThing] === true) {
                $("div.button-container[title='Snap to " + snapThing + "'] a div").click();
            }
        }

        leaflet.map.pm.enableDraw(
            'Polygon', {
            snappable: true,
            snapSegment: leaflet.getSmartSnapSetting("segments"),
            snapVertex: leaflet.getSmartSnapSetting("vertices"),
            allowSelfIntersection: false
        }
        );
    }

    leaflet.initGeojsonDownload = function () {
        function saveToFile(content, filename) {
            var file = filename + '.geojson';
            saveAs(new File([JSON.stringify(content)], file, {
                type: "text/plain;charset=utf-8"
            }), file);
        }

        L.easyButton(
            '<span class = DownArrowBar style = "font-size: 1.5em;">&DownArrowBar;</span>',
            function (btn, map) {
                leaflet.refreshParcels();
                let shapes = leaflet.parcels.toGeoJSON();
                console.log('Parcel data:', shapes)
                saveToFile(shapes, `${TRIM.store.currentScenario.name}_parcels`)
            },
            'Download parcel geojson'
        ).addTo(leaflet.map);
    };

    leaflet.initGeojsonUpload = function () {
        L.easyButton(
            '<span class = UpArrowBar style = "font-size: 1.5em;">&UpArrowBar;</span>',
            function (btn, map) {
                var input = document.createElement('input');
                input.type = 'file';

                input.onchange = e => {
                    // getting a hold of the file reference
                    var file = e.target.files[0];
                    if (file.name.split('.').pop() == "geojson") {
                        // setting up the reader
                        var reader = new FileReader();
                        reader.readAsText(file, 'UTF-8');

                        // here we tell the reader what to do when it's done reading...
                        reader.onload = readerEvent => {
                            var fileContent = readerEvent.target.result; // this is the content!
                            shapesJson = JSON.parse(fileContent);

                            let fieldData = [{
                                "type": "input",
                                "name": "geojson",
                                "value": JSON.stringify(shapesJson["features"])
                            }];

                            fieldData.push({
                                "type": "input",
                                "name": "scenario_id",
                                "value": TRIM.store.currentScenario.id
                            });

                            LoadingScreen.show('upload_parcel_geojson');
                            TRIM.api.uploadParcelFile(fieldData, function (success, responseData, c) {
                                LoadingScreen.hide('upload_parcel_geojson');

                                if (!success) {
                                    //alert('An error occurred during upload.');
                                    alert(responseData?.message)
                                    console.log(responseData)
                                    console.log(c)
                                } else {
                                    console.log("reload...");
                                    window.location.reload();
                                }
                            });
                        }
                    }
                    else if (file.name.split('.').pop() == "shp") {
                        console.log("This is a ShapeFile")
                        var shpfile = new L.Shapefile('shpFile/Durham.zip', {
                            onEachFeature: function (feature, layer) {
                                if (feature.properties) {
                                    layer.bindPopup(Object.keys(feature.properties).map(function (k) {
                                        return k + ": " + feature.properties[k];
                                    }).join("<br />"), {
                                        maxHeight: 200
                                    });
                                }
                            }
                        });
                        shpfile.addTo(leaflet.map);
                    }
                }
                input.click();
            },
            'Upload parcel geojson'
        ).addTo(leaflet.map);
    }
    // additional leaflet buttons -- END

    // aermod receptors -- START
    leaflet.initAermodReceptors = function () {
        LoadingScreen.show('check_aermod_receptors_file');
        TRIM.api.checkMiscScenarioFile(TRIM.store.currentScenario.id, "generated_aermod_receptors", function (success, responseData) {
            LoadingScreen.hide('check_aermod_receptors_file');
            if (!success) {
                console.log('An error occurred while fetching aermod receptors');
            } else {
                leaflet.renderAermodDownloadUi(responseData);
            }
        });
    }

    leaflet.installAermodReceptors = function (responseData, presignedGeojsonUrl) {
        let errorDisplayArea = $("#aermod-receptors-current-file .errors");
        errorDisplayArea.empty();

        let preserveShownState = receptorOverlayShowing;
        if (receptorOverlayGroup !== null) {
            mapLayers.removeLayer(receptorOverlayGroup); // removes option from the layers dialog
            receptorOverlayGroup.removeFrom(leaflet.map); // removes dots from the map
        }

        receptorOverlayGroup = L.layerGroup();

        if (presignedGeojsonUrl === undefined) {
            return;
        }
        if (responseData.file_metadata?.errors === undefined || responseData.file_metadata?.errors.length == 0) {
            TRIM.api.hitUrl(presignedGeojsonUrl, function (presignedSuccess, presignedResponse) {
                let overlayGridPoints = [];
                if (presignedResponse != null) {
                    for (let i = 0; i < presignedResponse.features.length; i++) {
                        let el = presignedResponse.features[i];
                        let point = [el.geometry.coordinates[1], el.geometry.coordinates[0]];
                        overlayGridPoints.push(point);
                        let colorForDisplay = "#000000"; // black
                        var marker = L.circleMarker(point, { pmIgnore: true, radius: .2, stroke: true, color: colorForDisplay }).addTo(receptorOverlayGroup);
                    }
                }

                receptorOverlayGroup.on("add", function () { receptorOverlayShowing = true; });
                receptorOverlayGroup.on("remove", function () { receptorOverlayShowing = false; });

                // preserve previously selected state after a refresh or regeneration
                if (preserveShownState) {
                    receptorOverlayGroup.addTo(leaflet.map); // preselects it in the layers control!
                }
            });

            mapLayers.addOverlay(receptorOverlayGroup, "AERMOD Receptors");
        }
        else {
            $("<h4/>").html("Errors with generated file:").appendTo(errorDisplayArea);
            if (responseData.file_metadata?.errors != undefined) {
                for (let i = 0; i < responseData.file_metadata.errors.length; i++) {
                    $("<li/>").html(responseData.file_metadata.errors[i]).appendTo(errorDisplayArea);
                }
            }
        }
    };

    leaflet.renderAermodDownloadUi = function (responseData) {
        let presignedGeojsonUrl = responseData.presigned_urls["data.geojson"];
        let presignedAermodInputUrl = responseData.presigned_urls["aermod_receptors.txt"];

        // update generate button label
        $("#generate_aermod_receptors_btn").html((presignedGeojsonUrl === undefined ? "Generate" : "Regenerate") + " AERMOD Receptors");

        // show the download URL
        if (presignedGeojsonUrl != undefined) {
            $("#aermod-receptors-download-geojson-btn").attr("href", presignedGeojsonUrl);
            $("#aermod-receptors-download-aermod-btn").attr("href", presignedAermodInputUrl);
            $("#aermod-receptors-current-file").show();
        }

        //plot it
        leaflet.installAermodReceptors(responseData, presignedGeojsonUrl);
    };
    // aermod receptors -- END

    // deposition overlay -- START
    leaflet.initDepositionOverlay = function () {
        LoadingScreen.show('check_overlay_status');
        TRIM.api.checkMiscScenarioFile(TRIM.store.currentScenario.id, "deposition_overlay", function (success, responseData) {
            LoadingScreen.hide('check_overlay_status');
            if (!success) {
                console.log('An error occurred while fetching overlay data');
            } else {
                TRIM.leaflet.installDepositionOverlayOntoMap(responseData)
            }
        });
    }

    leaflet.addDepositionOverlayLegend = function (bucketRanges, bucketColors) {
        if (typeof depositionOverlayLegend != "undefined") {
            leaflet.map.removeControl(depositionOverlayLegend); // removes the legend
        }

        // thx https://codepen.io/haakseth/pen/KQbjdO
        depositionOverlayLegend = L.control({ position: "bottomright" });

        depositionOverlayLegend.onAdd = function () {
            var div = L.DomUtil.create("div", "leaflet-legend deposition-overlay");

            div.innerHTML += "<h4>Total Deposition (g/m<sup>2</sup>)</h4>";
            for (let i = quartileGradient.length - 1; i >= 0; i--) {
                let jenksBucket = bucketRanges[i];
                let rangeDisplay = jenksBucket.from.toExponential() + " - " + jenksBucket.to.toExponential();
                div.innerHTML += '<i style="background: ' +
                    quartileGradient[i] +
                    '"></i><span>' +
                    rangeDisplay +
                    '</span><br>';
            }

            return div;
        };

        depositionOverlayLegend.addTo(leaflet.map);
    };


    leaflet.installDepositionOverlayOntoMap = function (responseData) {
        let errorDisplayArea = $("#deposition-overlay-current-file .errors");
        errorDisplayArea.empty();

        if (responseData.file_metadata == null) {
            return;
        }
        // show the management UI
        $("#deposition-overlay-current-filename").html(responseData.file_metadata.original_file_name);
        $("#deposition-overlay-current-file").show();

        if (responseData.file_metadata.errors === undefined || responseData.file_metadata.errors.length == 0) {
            let presignedUrl = responseData.presigned_urls["processed.json"];
            TRIM.api.hitUrl(presignedUrl, function (presignedSuccess, presignedResponse) {
                let overlayPolyPoints = [];
                for (let i = 0; i < presignedResponse.row_data.length; i++) {
                    let el = presignedResponse.row_data[i];
                    let point = [el.wgs84_lat, el.wgs84_long];
                    overlayPolyPoints.push(point);
                    let colorForDisplay = quartileGradient[el.jenks_bucket];
                    var marker = L.circleMarker(point, { pmIgnore: true, radius: 1, stroke: true, color: colorForDisplay }).bindPopup("Total Depo == " + el.combined_deposition.toExponential()).addTo(depositionOverlayGroup);
                }

                leaflet.addDepositionOverlayLegend(responseData.file_metadata.jenks_buckets, quartileGradient);

                depositionOverlayGroup.on("add", function () { $(".leaflet-legend").removeClass("hidden"); });
                depositionOverlayGroup.on("remove", function () { $(".leaflet-legend").addClass("hidden"); });
                depositionOverlayGroup.addTo(leaflet.map); // preselects it in the layers control!
            });
            mapLayers.addOverlay(depositionOverlayGroup, "Deposition");
        } else {
            $("<h4/>").html("Errors with uploaded file:").appendTo(errorDisplayArea);
            for (let i = 0; i < responseData.file_metadata.errors.length; i++) {
                $("<li/>").html(responseData.file_metadata.errors[i]).appendTo(errorDisplayArea);
            }
        }
    };

    leaflet.removeDepositionOverlayFromMap = function () {
        if (typeof depositionOverlayLegend != "undefined") {
            leaflet.map.removeControl(depositionOverlayLegend); // removes the legend
        }
        mapLayers.removeLayer(depositionOverlayGroup); // removes from the layers menu
        depositionOverlayGroup.removeFrom(leaflet.map); // hides from the map
        $("#deposition-overlay-current-file").hide(); // hide management ui
    };
    // deposition overlay  -- END

    trim.leaflet = leaflet;
    return trim;
})(window.TRIM || {});