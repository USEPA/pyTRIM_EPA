
window.MIRC = ((mirc) => {
    // ===========================
    // MIRC.API
    // ===========================

    const ajaxCall = (opts) => {
        const method = opts.method || 'GET';
        const url = opts.url || '';
        const data = opts.data || null;

        const request = new XMLHttpRequest();
        request.open(method, url);
        request.send(data);

        return new Promise((resolve, reject) => {
            request.onload = (e) => {
                try {
                    const data = JSON.parse(request.responseText);
                    resolve(data);
                }
                catch {
                    reject(request);
                }
            };
            request.onerror = (e) => {
                reject(request);
            };
        });
    };

    let endpoints = {};

    const API = {
        async reloadApiMap() {
            return ajaxCall({url: '/api/'}).then((data) => {
                endpoints = data.endpoints || {};
            });
        },

        async getEndpoint(name, params) {
            if (!endpoints.api_map) {
                await this.reloadApiMap();
            }
            const endpoint = name.split('.', 2);
            const group = endpoint[0];
            if (!endpoints[group]) {
                return null;
            }

            let urlInfo = {};
            if (endpoint.length > 1) {
                urlInfo = endpoints[group][endpoint[1]];
            }
            else {
                urlInfo = endpoints[group];
            }

            let url = urlInfo.url;
            const methods = urlInfo.methods;

            if (params !== undefined) {
                const queryParams = {...params}
                for (const key in params) {
                    const p = `:${key}>`;
                    if (url.indexOf(p) >= 0) {
                        url = url.replace(p, queryParams[key])
                        delete queryParams[key];
                    }
                }
                url = url.replace(/<int/g, '');
                url = url.replace(/<string/g, '');

                if (queryParams) {
                    url += '?';
                    const urlParams = [];
                    for (const key in queryParams) {
                        let vals = queryParams[key];
                        if (!Array.isArray(vals)) {
                            vals = [vals];
                        }
                        for (const v of vals) {
                            urlParams.push(`${key}=${v}`);
                        }
                    }
                    url += urlParams.join('&');
                }
            }

            return {url, methods};
        },

        async call(opts) {
            const method = opts.method || 'GET';
            const data = opts.data;
            let url = opts.url;

            if (!url) {
                const endpointInfo = await this.getEndpoint(opts.endpoint, opts.parameters);
                url = endpointInfo.url;
                if (
                    endpointInfo.methods.indexOf(method) < 0 &&
                    method.toUpperCase() != 'GET'
                ) {
                    throw `${method} is not an allowed method for ${opts.endpoint}`;
                }
            }

            return ajaxCall({url, method, data});
        }
    };

    mirc.API = API;
    
    // ===========================
    // MIRC.FORMS
    // ===========================

    const updateSelect = (select, options) => {
        if (typeof(select) === typeof('')) {
            select = document.getElementById(select);
        }

        select.innerHTML = '';

        const defaultVal = select.getAttribute('data-default') || undefined;

        let selectIndex = -1;
        for (const o of options) {
            let opt = o;
            if (typeof(o) == typeof('')) {
                opt = {value: o, label: o};
            }
            else if (Array.isArray(o)) {
                opt = {value: o[0], label: o[1]}
            }
            var option = document.createElement('option');
            option.value = opt.value;
            option.innerText = opt.label;
            select.appendChild(option);

            if (defaultVal !== undefined && defaultVal == opt.value) {
                selectIndex = select.children.length - 1;
            }
        }
        select.selectedIndex = selectIndex;
    };

    const getSelectedValue = (select) => {
        const val = select.options[select.selectedIndex].value;
        return val;
    };

    const setSelectedValue = (select, value) => {
        for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value == value) {
                select.selectedIndex = i;
                break;
            }
        }
    };

    const formLoadEvent = (() => {
        const e = document.createEvent('Event');
        e.initEvent('form:loaded', true, true);
        return e;
    })();

    const loadJsonForm = async (names) => {
        if (!names) {
            return undefined;
        }
        if (!Array.isArray(names)) {
            names = [names];
        }
        names = names.slice(0); // clone array

        return await API.call({
            endpoint: 'file_api.get_json_forms',
            parameters: {
                form: names
            }
        });
    };

    const loadAsyncForm = async (template, src) => {
        const formData = await loadJsonForm(src);
        if (formData && formData[src]) {
            drawForm(formData[src], template);
            template.classList.add('form-loaded');
            template.dispatchEvent(formLoadEvent);
            updateDefaults(template);
        }
    };

    const drawForm = (data, template, prefix) => {
        if (!template.tagName.toLowerCase() == 'form' &&
            !template.hasAttribute('data-slot')) {
            return;
        }

        if (!template.hasAttribute('data-async-form')) {
            template.setAttribute('data-async-form', 'true');
        }

        const titleSlot = template.querySelectorAll(
            `[data-slot][data-target="title"]`
        )[0];
        if (titleSlot) {
            titleSlot.innerHTML = data.title;
        }

        const fields = data.fields || [];
        for (const f of fields) {
            const slot = template.querySelectorAll(
                `[data-slot][data-target="${f.id}"]`
            )[0];
            if (slot) {
                if (f.data_type == 'form') {
                    drawForm(f.form_definition, slot, f.id + (f.seperator || '_'));
                }
                else {
                    const elem = renderField(f, prefix, slot);
                    if (elem) {
                        slot.outerHTML = elem.outerHTML;
                    }
                }
            }
        }
    };

    const renderField = (fieldDef, prefix, template) => {
        fieldDef.id = (prefix || '') + (fieldDef.id || '');
        const group = document.createElement('div');
        group.className = 'form-group';

        if (fieldDef.data_type == 'field_list') {
            const wrapper = renderFieldList(fieldDef, template);
            group.innerHTML = wrapper.innerHTML;
        }
        else {
            const wrapper = renderSingleField(fieldDef, template);
            group.innerHTML = wrapper.innerHTML;

            const description = fieldDef.description;
            if (description) {
                const desc = document.createElement('small');
                desc.className = 'form-text text-muted';
                desc.innerHTML = description;
                group.appendChild(desc);
            }
        }

        return group;
    };

    const renderFieldList = (fieldListDef, template) => {
        const wrapper = document.createElement('div');

        const minEntries = fieldListDef.min_entries || 0;

        const fieldset = document.createElement('fieldset');
        fieldset.id = fieldListDef.id;
        fieldset.className = 'card';
        fieldset.setAttribute('data-value', '[]');
        fieldset.setAttribute('data-label', fieldListDef.field.label);
        fieldset.setAttribute('data-min-entries', minEntries);

        const header = renderFieldListHeader(fieldListDef);
        fieldset.appendChild(header);

        const body = document.createElement('div');
        body.className = 'card-body p-2 pb-0';

        const nav = renderFieldListNav(fieldListDef);
        body.appendChild(nav);

        const tabContent = renderFieldListTabs(fieldListDef, template);
        body.appendChild(tabContent);

        fieldset.appendChild(body);

        for (let i = 0; i < minEntries; i++) {
            addTabToFieldList(fieldset);
        }

        wrapper.appendChild(fieldset);
        return wrapper;
    };

    const renderFieldListHeader = (fieldListDef) => {
        const header = document.createElement('div');
        header.className = 'card-header d-flex py-2 pl-3 pr-2';

        const title = document.createElement('span');
        title.className = 'pt-1';
        title.innerHTML = fieldListDef.label;
        header.appendChild(title);

        const add = document.createElement('ul');
        add.className = 'nav ml-auto';

        const addLi = document.createElement('li');
        addLi.className = 'nav-item';

        const addBtn = document.createElement('a');
        addBtn.id = fieldListDef.id + '-add-btn';
        addBtn.href = '#add';
        addBtn.className = 'nav-link py-1 px-2 border-primary border rounded';
        addBtn.title = 'Add';
        addBtn.setAttribute('data-fieldlist-add', 'true');
        addBtn.innerHTML = '<i class="fa fa-plus"></i>&nbsp;Add';

        addLi.appendChild(addBtn);
        add.appendChild(addLi);
        header.appendChild(add);

        return header;
    }

    const renderFieldListNav = (fieldListDef) => {
        const nav = document.createElement('nav');
        nav.className = 'mb-2 px-2';

        const pills = document.createElement('ul');
        pills.id = fieldListDef.id + '-pills';
        pills.className = 'nav nav-pills';

        const pillTemplate = document.createElement('li');
        pillTemplate.className = 'nav-item';
        pillTemplate.setAttribute('data-template', 'true');
        pillTemplate.style.display = 'none';

        const navBtn = document.createElement('a');
        navBtn.id = fieldListDef.id + '-##-pill';
        navBtn.href = '#' + fieldListDef.id + '-##-tab';
        navBtn.className = 'nav-link p-2';
        navBtn.setAttribute('data-toggle', 'pill');
        navBtn.setAttribute('aria-controls', fieldListDef.id + '-##-tab');
        navBtn.setAttribute('aria-selected',  'false');
        navBtn.innerHTML = fieldListDef.field.label + '&nbsp;<span>#pillnum;</span>';

        pillTemplate.appendChild(navBtn);
        pills.appendChild(pillTemplate);

        nav.appendChild(pills);

        return nav;
    }

    const renderFieldListTabs = (fieldListDef, template) => {
        const tabContent = document.createElement('div');
        tabContent.id = fieldListDef.id + '-tabs';
        tabContent.className = 'tab-content';

        const tabTemplate = document.createElement('div');
        tabTemplate.id = fieldListDef.id + '-##-tab';
        tabTemplate.className = 'tab-pane pt-3 px-2 border-top';
        tabTemplate.style.display = 'none';
        tabTemplate.setAttribute('role', 'tabpanel');
        tabTemplate.setAttribute('aria-labelledby', fieldListDef.id + '-##-pill');
        tabTemplate.setAttribute('data-template', 'true');

        if (fieldListDef.field.data_type === 'form') {
            const formDef = fieldListDef.field.form_definition;
            const sep = fieldListDef.field.seperator || '_';

            tabTemplate.innerHTML = template.innerHTML;

            drawForm(formDef, tabTemplate, fieldListDef.id + '-##' + sep)
        }
        else {
            const fieldDef = fieldListDef.field;
            const elem = renderField(fieldDef, fieldListDef.id + '-##');
            if (elem) {
                tabTemplate.innerHTML = elem.outerHTML;
            }
        }

        const rem = document.createElement('div');
        rem.className = 'text-center';
        rem.style.display = 'none';

        const remBtn = document.createElement('a');
        remBtn.href = '#remove-' + fieldListDef.id + '-##-tab';
        remBtn.className = 'btn btn-sm btn-outline-danger';
        remBtn.title = 'Remove';
        remBtn.setAttribute('data-fieldlist-rem', 'true');
        remBtn.innerHTML = 'Remove ' + fieldListDef.field.label;

        rem.appendChild(remBtn);
        tabTemplate.appendChild(rem);

        tabContent.appendChild(tabTemplate);

        return tabContent;
    }

    const addTabToFieldList = (fieldset) => {
        const values = JSON.parse(fieldset.getAttribute('data-value'));
        const label = fieldset.getAttribute('data-label');
        const id = fieldset.id;

        const repl = new RegExp(id + '-##', 'g');
        const next = id + '-' + values.length;

        const nav = fieldset.querySelector('.nav.nav-pills'); 
        const pillTemplate = nav.querySelector('[data-template]');

        for (const child of nav.children) {
            if (child.className.indexOf('nav-item') < 0) {
                continue;
            }
            const a = child.getElementsByTagName('a')[0];
            a.classList.remove('active');
        }

        const pillWrapper = document.createElement('div');
        pillWrapper.innerHTML = pillTemplate.outerHTML
            .replace(repl, next).replace(/#pillnum;/g, values.length + 1);

        const newPill = pillWrapper.children[0];
        newPill.removeAttribute('data-template');
        newPill.setAttribute('data-pill-id', values.length);
        newPill.style.display = '';
        newPill.getElementsByTagName('a')[0].classList.add('active');
        nav.appendChild(newPill);

        const tabs = fieldset.querySelector('.tab-content');
        const tabTemplate = tabs.querySelector('[data-template]');

        for (const child of tabs.children) {
            if (child.className.indexOf('tab-pane') < 0) {
                continue;
            }
            child.className = child.className.replace('show active', ' ')
        }

        const tabWrapper = document.createElement('div');
        tabWrapper.innerHTML = tabTemplate.outerHTML.replace(repl, next);

        const newTab = tabWrapper.children[0];
        newTab.removeAttribute('data-template');
        newTab.setAttribute('data-tab-id', values.length);
        newTab.className += ' show active';
        newTab.style.display = '';

        const remBtn = newTab.querySelector(
            '[data-fieldlist-rem][href="#remove-' + newTab.id + '"]');
        const minEntries = fieldset.getAttribute('data-min-entries');
        if (values.length >= parseInt(minEntries)) {
            remBtn.parentElement.style.display = '';
        }

        tabs.appendChild(newTab);


        values.push(1);
        fieldset.setAttribute('data-value', JSON.stringify(values));
    }

    const removeTabFromFieldList = (fieldset, i) => {
        const values = JSON.parse(fieldset.getAttribute('data-value'));

        const nav = fieldset.querySelector('.nav.nav-pills');
        nav.removeChild(nav.querySelector('[data-pill-id="' + i + '"]'));
        for (const child of nav.children) {
            if (child.hasAttribute('data-template')) {
                continue;
            }
            const a = child.getElementsByTagName('a')[0];
            a.classList.add('active');
            break;
        }

        const tabs = fieldset.querySelector('.tab-content');
        tabs.removeChild(tabs.querySelector('[data-tab-id="' + i + '"]'));
        for (const child of tabs.children) {
            if (child.hasAttribute('data-template')) {
                continue;
            }
            child.className += ' show active';
            break;
        }

        values.splice(i, 1);
        fieldset.setAttribute('data-value', JSON.stringify(values));
    }

    const renderSingleField = (fieldDef, template) => {
        const wrapper = template || document.createElement('div');

        const boolTypes = ['boolean', 'bool', 'bit', 'bitwise'];
        if (boolTypes.indexOf(fieldDef.data_type) >= 0) {
            field = renderCheckBoxInput(fieldDef);
            wrapper.insertBefore(field, wrapper.firstChild);
            return wrapper;
        }

        let label = null;
        if (fieldDef.label) {
            label = renderLabel(fieldDef);
        }

        let field = null;
        if (fieldDef.data_type == 'file') {
            field = renderFileInput(fieldDef);
        }
        else {
            field = renderInput(fieldDef);
        }

        const fieldCls = wrapper.getAttribute('data-field-cls');
        if (fieldCls != null) {
            if (fieldCls.indexOf('form-control-plaintext') > -1) {
                field.classList.remove('form-control');
                field.classList.remove('form-control-sm');
            }
            field.className = [field.className, fieldCls].join(' ');
        }
        wrapper.insertBefore(field, wrapper.firstChild);

        if (label) {
            const lblCls = wrapper.getAttribute('data-label-cls');
            if (lblCls != null) {
                field.className = [field.className, lblCls].join(' ');
            }
            wrapper.insertBefore(label, field);
        }

        const errs = document.createElement('div');
        errs.id = fieldDef.id + '-feedback';
        errs.className = 'invalid-feedback';
        wrapper.appendChild(errs);

        return wrapper;
    };

    const renderCheckBoxInput = (fieldDef) => {
        const id = fieldDef.id;

        const field = document.createElement('div');
        field.className = 'custom-control custom-checkbox form-check-inline';

        const inner = document.createElement('input');
        inner.type = 'checkbox';
        inner.id = id;
        inner.name = id;
        inner.className = 'custom-control-input';
        inner.style.maxWidth = '100%';
        field.appendChild(inner);

        if (fieldDef.default !== undefined) {
            if (fieldDef.default || false) {
                inner.setAttribute('checked', 'checked');
            }
            else {
                inner.removeAttribute('checked');
            }
        }

        const innerLabel = renderLabel(fieldDef);
        innerLabel.className = 'custom-control-label';
        field.appendChild(innerLabel);
        
        if (fieldDef.readonly) {
            inner.setAttribute('readonly', 'readonly');
            innerLabel.setAttribute('readonly', 'readonly');
        }

        return field;
    };

    const renderLabel = (fieldDef) => {
        const id = fieldDef.id;
        const labelText = fieldDef.label;
        const req = fieldDef.required;
        const help = fieldDef.help;

        const label = document.createElement('label');
        label.htmlFor = id;

        if (req) {
            const required = document.createElement('span');
            required.style.color = 'firebrick';
            required.innerHTML = '*&nbsp;';
            label.appendChild(required);
        }

        const txt = document.createElement('span');
        txt.innerHTML = labelText + '&nbsp';
        label.appendChild(txt);

        if (help) {
            const helpElements = renderHelpElements(help);
            label.appendChild(helpElements.marker);
            label.appendChild(helpElements.helpTxt);
        }
        return label;
    }

    const renderHelpElements = (help) => {
        const marker = document.createElement('sup');

        const toggle = document.createElement('a');
        toggle.href = '#help-' + id;
        toggle.setAttribute('role', 'button');
        toggle.setAttribute('data-toggle', 'collapse');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-controls', 'help-' + id);

        const hov = document.createElement('span');
        hov.title = 'Click here for additional instructions';

        const symbol = document.createElement('i');
        symbol.className = 'fa fa-question';

        hov.appendChild(symbol);
        toggle.appendChild(hov);
        marker.appendChild(toggle);

        const helpTxt = document.createElement('div');
        helpTxt.id = 'help-' + id;
        helpTxt.className = 'collapse';

        const muted = document.createElement('small');
        muted.className = 'form-text text-muted';
        muted.innerHTML = help;
        helpTxt.appendChild(muted);

        return {marker, helpTxt};
    };

    const renderFileInput = (fieldDef) => {
        const id = fieldDef.id;

        const field = document.createElement('div');
        field.className = 'custom-file';

        const inner = document.createElement('input');
        inner.type = 'file';
        inner.id = id;
        inner.name = id;
        if (fieldDef.multiple) {
            inner.setAttribute('multiple', 'multiple');
        }
        inner.className = 'custom-file-input';
        inner.style.maxWidth = '100%';
        field.appendChild(inner);

        const innerLabel = document.createElement('label');
        innerLabel.className = 'custom-file-label form-control-sm';
        innerLabel.htmlFor = id;
        if (fieldDef.multiple) {
            innerLabel.innerText = 'Choose files';
        }
        else {
            innerLabel.innerText = 'Choose file';
        }
        field.appendChild(innerLabel);

        if (fieldDef.readonly) {
            inner.setAttribute('readonly', 'readonly');
            innerLabel.setAttribute('readonly', 'readonly');
        }

        if (fieldDef.class) {
            field.className += ' ' + fieldDef.class;
        }

        return field;
    }

    const renderInput = (fieldDef) => {
        const id = fieldDef.id;
        const dataType = fieldDef.data_type;
        const widget = fieldDef.widget;
        const defaultVal = fieldDef.default;

        let field = document.createElement('input');
        if (widget == 'select') {
            field = document.createElement('select');
            if (fieldDef.multiple === true) {
                field.setAttribute('multiple', 'multiple');
            }
            if (defaultVal !== undefined) {
                field.setAttribute('data-default', defaultVal);
            }
            updateSelect(field, fieldDef.choices);
        }
        else if (widget == 'radio') {
            return renderRadioList(fieldDef);
        }
        else if (widget == 'textarea') {
            field = document.createElement('textarea');
            if (defaultVal) {
                field.innerText = defaultVal;
            }
        }
        else {
            let type = dataType;
            if (type == 'int' || type == 'float') {
                type = 'number';
            }
            else if (type == 'datetime') {
                type = 'datetime-local';
            }
            else if (type == 'string' || type === undefined) {
                type = 'text';
            }
            field.type = type;
            if (defaultVal !== undefined) {
                field.setAttribute('value', defaultVal);
            }
            if (fieldDef.min !== undefined) {
                field.setAttribute('min', fieldDef.min);
            }
            if (fieldDef.max !== undefined) {
                field.setAttribute('max', fieldDef.max);
            }
            if (fieldDef.step !== undefined) {
                field.setAttribute('step', fieldDef.step);
            }
        }
        field.id = id;
        field.name = id;
        field.className = 'form-control form-control-sm';
        field.style.maxWidth = '100%';

        if (fieldDef.class) {
            field.className += ' ' + fieldDef.class;
        }

        if (fieldDef.readonly) {
            field.setAttribute('readonly', 'readonly');
        }
        if (fieldDef.disabled) {
            field.setAttribute('disabled', 'disabled');
        }

        return field;
    };

    const renderRadioList = (fieldDef) => {
        const wrapper = document.createElement('div');

        const defaultVal = fieldDef.default;

        let i = 0;
        for (const choice of fieldDef.choices) {
            let opt = choice;
            if (typeof(opt) == typeof('')) {
                opt = {value: opt, label: opt};
            }
            else if (Array.isArray(opt)) {
                opt = {value: opt[0], label: opt[1]};
            }

            const group = document.createElement('div');
            group.className = 'custom-control custom-radio';

            const field = document.createElement('input');
            field.type = 'radio';
            field.className = 'custom-control-input';
            field.id = fieldDef.id + '-' + i;
            field.name = fieldDef.id;
            field.value = opt.value;

            if (field.value == defaultVal) {
                field.setAttribute('checked', 'checked');
            }

            group.appendChild(field);

            const label = document.createElement('label');
            label.className = 'custom-control-label';
            label.htmlFor = fieldDef.id + '-' + i;
            label.innerText = opt.label;

            group.appendChild(label);

            wrapper.appendChild(group);
            i++;
        }

        return wrapper;
    }

    const updateDefaults = (form) => {
        const inputs = form.getElementsByTagName('input');
        for (const input of inputs) {
            const defaultVal = input.getAttribute('data-default');
            if (defaultVal) {
                input.value = defaultVal;
            }
        }
        const selects = form.getElementsByTagName('select');
        for (const select of selects) {
            const defaultVal = select.getAttribute('data-default');
            if (defaultVal) {
                setSelectedValue(select, defaultVal);
            }
        }
    };

    const registerEvents = () => {
        // Create a global event listener for when custom file inputs
        // change their value
        document.body.addEventListener('change', function(e) {
            if (e.target.className.indexOf('custom-file-input') < 0) {
                return;
            }
            const lbl = e.target.parentElement.getElementsByTagName('label')[0];
            if (e.target.hasAttribute('multiple')) {
                let files = [...e.target.files];
                if (files.length) {
                    lbl.innerText = `${files.length} files`;
                }
                else {
                    lbl.innerText = 'Choose files';
                }
            }
            else {
                let val = e.target.value;
                if (val.toString().trim()) {
                    val = val.toString().split('/');
                    val = val[val.length - 1];
                    val = val.toString().split('\\');
                    val = val[val.length - 1];
                    lbl.innerText = val;
                }
                else {
                    lbl.innerText = 'Choose file';
                }
            }
        });

        // Create a global event listener for adding to field lists
        document.body.addEventListener('click', function(e) {
            const btn = e.target.closest('a');
            if (btn == null || !btn.hasAttribute('data-fieldlist-add')) {
                return;
            }
            e.preventDefault();

            const fieldset = btn.closest('fieldset');
            addTabToFieldList(fieldset);
        });
        // Create a global event listener for removing from field lists
        document.body.addEventListener('click', function(e) {
            const btn = e.target.closest('a');
            if (btn == null || !btn.hasAttribute('data-fieldlist-rem')) {
                return;
            }
            e.preventDefault();

            const num = btn.closest('.tab-pane').getAttribute('data-tab-id');

            const fieldset = btn.closest('fieldset');
            removeTabFromFieldList(fieldset, parseInt(num));
        });

        // On dom load, auto-draw forms that are labelled async
        document.addEventListener("DOMContentLoaded", function(e) {
            const formTemplates = document.getElementsByTagName('form');
            
            if (formTemplates.length) {
                // Throw up a loading screen
                window.LoadingScreen.show('async_form_loading');
            }

            const forms = [];
            for (const template of formTemplates) {
                if (!template.getAttribute('data-async-form')) {
                    continue;
                }
                const src = template.getAttribute('data-form-src')
                if (!src) {
                    continue;
                }
                forms.push(loadAsyncForm(template, src));
            }
            Promise.all(forms).then(() => {
                window.LoadingScreen.hide('async_form_loading');
            }).catch(() => {
                window.LoadingScreen.hide('async_form_loading');
            });
        });
    };

    const FORMS = {
        formLoadEvent,
        loadJsonForm,
        loadAsyncForm,
        draw: drawForm,
        render: renderField,
        registerEvents
    };

    class FieldListTabs {
        constructor(opts) {
            this.element = opts.element;
            this.minEntries = opts.minEntries || 0;
            this.maxEntries = opts.maxEntries || Infinity;

            this.__next = this.tabs().length;

            this.init();
        }

        init() {
            const firstTab = this.element.querySelectorAll('.tab-pane')[0];
            const firstPref = this.getPref(firstTab.getAttribute('data-index'));

            const repl = new RegExp(firstPref, 'g');
            const dummyPref = this.getPref('##');

            this.tabTemplate = firstTab.outerHTML.replace(repl, dummyPref);

            const firstPill = this.element.querySelectorAll('nav .nav-item')[0];
            this.pillTemplate = firstPill.outerHTML.replace(repl, dummyPref);

            const cardBody = this.element.querySelector('.card-body');
            cardBody.style.display = '';

            this.switchToTab(0);
        }

        tabs() {
            return this.element.querySelectorAll('.tab-pane');
        }

        currentTab() {
            return this.element.querySelector('.tab-pane.active');
        }

        currentId() {
            const tab = this.currentTab();
            if (tab != null) {
                return tab.getAttribute('data-index');
            }
            return null;
        }

        nextId() {
            return this.__next;
        }

        getPref(id) {
            if (id === undefined) {
                id = this.nextId();
            }
            return this.element.id + '-' + id;
        }

        isValidId(id) {
            const tab = this.element.querySelector(`.tab-pane[data-index="${id}"]`)
            if (tab == null) {
                return false;
            }
            return true;
        }

        addTab(template) {
            if (this.tabs().length >= this.maxEntries) {
                console.warn(
                    'Cannot add a new entry; the maximum number of entries has been reached.'
                    )
                return;
            }

            const repl = new RegExp(this.getPref('##'), 'g');
            const pref = this.getPref();

            const temp = document.createElement('div');

            const nav = this.element.querySelector('nav ul');
            temp.innerHTML = this.pillTemplate.replace(repl, pref);
            const newPill = temp.querySelector('li');
            newPill.querySelector('a').setAttribute('data-index', this.nextId());
            newPill.querySelector('span').innerText = this.nextId() + 1;
            nav.appendChild(newPill);

            if (template === undefined) {
                template = this.tabTemplate;
            }

            const tabs = this.element.querySelector('.tab-content');
            temp.innerHTML = template.replace(repl, pref);
            const newTab = temp.querySelector('div');
            newTab.setAttribute('data-index', this.nextId());
            tabs.appendChild(newTab);

            this.switchToTab(this.nextId());
            this.__next++;
        }

        cloneTab(id) {
            if (id === undefined) {
                id = this.currentId();
            }
            else {
                this.switchToTab(id);
            }

            if (!this.isValidId(id)) {
                return;
            }

            const tab = this.currentTab();
            const pref = this.getPref(tab.getAttribute('data-index'));
            const repl = new RegExp(pref, 'g');

            const template = tab.outerHTML.replace(repl, this.getPref('##'));

            this.addTab(template);

            const newTab = this.currentTab();
            const newPref = this.getPref(newTab.getAttribute('data-index'));

            for (const select of tab.querySelectorAll('select')) {
                const val = getSelectedValue(select);
                const n = document.getElementById(select.id.replace(repl, newPref));
                if (n) {
                    setSelectedValue(n, val);
                }
            }
            for (const field of tab.querySelectorAll('input, textarea')) {
                const val = field.value;
                const n = document.getElementById(field.id.replace(repl, newPref));
                if (n) {
                    n.value = val;
                }
            }
        }

        removeTab(id) {
            if (this.tabs().length <= this.minEntries) {
                console.warn(
                    'Cannot remove another entry; this is the minimum number of entries.'
                )
                return;
            }

            if (id === undefined) {
                id = this.currentId();
            }

            if (!this.isValidId(id)) {
                return;
            }

            const pref = this.getPref(id);

            const tab = document.getElementById(pref + '-tab');
            tab.parentNode.removeChild(tab);

            const pill = document.getElementById(pref + '-pill').closest('.nav-item');
            pill.parentNode.removeChild(pill);

            const deletedId = id;

            while (id > -1) {
                if (this.isValidId(id)) {
                    this.switchToTab(id);
                    return;
                }
                id--;
            }
            id = deletedId;
            while (id < this.nextId()) {
                if (this.isValidId(id)) {
                    this.switchToTab(id);
                    return;
                }
                id++;
            }
            this.switchToTab(null);
            this.__next = 0;
        }

        switchToTab(id) {
            if (!this.isValidId(id) && id !== null) {
                return;
            }

            const actions = this.element.querySelector('.tab-actions');
            actions.style.display = '';
            if (id === null) {
                actions.style.display = 'none';
                return;
            }

            const rem = actions.querySelector('.field-list-remove');
            rem.style.display = '';
            if (this.tabs().length <= this.minEntries) {
                rem.style.display = 'none';
            }

            const add = this.element.querySelector('.field-list-add').closest('li');
            add.style.display = '';
            if (this.tabs().length >= this.maxEntries) {
                add.style.display = 'none';
            }

            const btn = this.element.querySelector(`a[data-index="${id}"]`);
            btn.click();
        }
    }

    const initFieldListTabs = (opts) => {
        const handler = new FieldListTabs(opts);

        const element = opts.element

        element.addEventListener('click', (e) => {
            if (e.target.className.indexOf('field-list-add') < 0) {
                return;
            }
            e.preventDefault();
            handler.addTab();
        });
        element.addEventListener('click', (e) => {
            if (e.target.className.indexOf('field-list-copy') < 0) {
                return;
            }
            e.preventDefault();
            handler.cloneTab();
        });
        element.addEventListener('click', (e) => {
            if (e.target.className.indexOf('field-list-remove') < 0) {
                return;
            }
            e.preventDefault();
            handler.removeTab();
        });

        return handler;
    };

    FORMS.initFieldListTabs = initFieldListTabs;
    FORMS.registerEvents();

    mirc.FORMS = FORMS;

    return mirc;
})(window.MIRC || {});
