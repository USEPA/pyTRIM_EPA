
window.TRIM = (function(trim) {
    var forms = trim.forms || {};

    forms.updateSelect = function(select, options) {
        if (typeof(select) === typeof('')) {
            select = document.getElementById(select);
        }

        select.innerHTML = '';

        var defaultVal = select.getAttribute('data-default') || undefined;

        var selectIndex = -1;
        for (var i = 0, len = options.length; i < len; i++) {
            var opt = options[i];
            if (typeof(opt) == typeof('')) {
                opt = {label: opt, value: opt};
            }
            else if (Array.isArray(opt)) {
                opt = {label: opt[0], value: opt[1]}
            }
            var option = document.createElement('option');
            option.value = opt.value;
            option.innerText = opt.label;
            select.appendChild(option);

            if (defaultVal !== undefined && defaultVal == opt.value) {
                selectIndex = i;
            }
        }
        select.selectedIndex = selectIndex;
    };

    function renderLabel(fieldDef) {
        var id = fieldDef.id;
        var labelText = fieldDef.label;
        var req = fieldDef.required;
        var help = fieldDef.help;

        var label = document.createElement('label');
        label.htmlFor = id;

        if (req) {
            var required = document.createElement('span');
            required.style.color = 'firebrick';
            required.innerHTML = '*&nbsp;';
            label.appendChild(required);
        }

        var txt = document.createElement('span');
        txt.innerHTML = labelText + '&nbsp';
        label.appendChild(txt);

        if (help) {
            var marker = document.createElement('sup');

            var toggle = document.createElement('a');
            toggle.href = '#help-' + id;
            toggle.setAttribute('role', 'button');
            toggle.setAttribute('data-toggle', 'collapse');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-controls', 'help-' + id);

            var hov = document.createElement('span');
            hov.title = 'Click here for additional instructions';

            var symbol = document.createElement('i');
            symbol.className = 'fa fa-question';

            hov.appendChild(symbol);
            toggle.appendChild(hov);
            marker.appendChild(toggle);
            label.appendChild(marker);

            var helpContainer = document.createElement('div');
            helpContainer.id = 'help-' + id;
            helpContainer.className = 'collapse';

            var helpTxt = document.createElement('small');
            helpTxt.className = 'form-text text-muted';
            helpTxt.innerHTML = help;
            helpContainer.appendChild(helpTxt);

            label.appendChild(helpContainer);
        }
        return label;
    }

    function renderFileInput(fieldDef) {
        var id = fieldDef.id;

        var field = document.createElement('div');
        field.className = 'custom-file';

        var inner = document.createElement('input');
        inner.type = 'file';
        inner.id = id;
        inner.name = id;
        inner.className = 'custom-file-input';
        inner.style.maxWidth = '100%';
        field.appendChild(inner);

        var innerLabel = document.createElement('label');
        innerLabel.className = 'custom-file-label form-control-sm';
        innerLabel.htmlFor = id;
        innerLabel.innerText = 'Choose file';
        field.appendChild(innerLabel);

        if (fieldDef.readonly) {
            inner.setAttribute('readonly', 'readonly');
            innerLabel.setAttribute('readonly', 'readonly');
        }

        return field;
    }

    // Create a global event listener for when custom file inputs
    // change their value
    document.body.addEventListener('change', function(e) {
        if (e.target.className.indexOf('custom-file-input') < 0) {
            return;
        }
        var val = e.target.value;
        var lbl = e.target.parentElement.getElementsByTagName('label')[0];
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
    });

    function renderCheckBoxInput(fieldDef) {
        var id = fieldDef.id;

        var field = document.createElement('div');
        field.className = 'custom-control custom-checkbox form-check-inline';

        var inner = document.createElement('input');
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

        var innerLabel = renderLabel(fieldDef);
        innerLabel.className = 'custom-control-label';
        field.appendChild(innerLabel);
        
        if (fieldDef.readonly) {
            inner.setAttribute('readonly', 'readonly');
            innerLabel.setAttribute('readonly', 'readonly');
        }

        return field;
    }

    function renderInput(fieldDef) {
        var id = fieldDef.id;
        var dataType = fieldDef.data_type;
        var widget = fieldDef.widget;
        var defaultVal = fieldDef.default;

        var field = document.createElement('input');
        if (widget == 'select') {
            field = document.createElement('select');
            if (defaultVal !== undefined) {
                field.setAttribute('data-default', defaultVal);
            }
            forms.updateSelect(field, fieldDef.choices);
        }
        else if (widget == 'textarea') {
            field = document.createElement('textarea');
            if (defaultVal) {
                field.innerText = defaultVal;
            }
        }
        else {
            var type = dataType;
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

        if (fieldDef.readonly) {
            field.setAttribute('readonly', 'readonly');
        }

        return field;
    }

    function renderSingleField(fieldDef) {
        var wrapper = document.createElement('div');

        var boolTypes = ['boolean', 'bool', 'bit', 'bitwise'];
        if (boolTypes.indexOf(fieldDef.data_type) >= 0) {
            field = renderCheckBoxInput(fieldDef);
            wrapper.appendChild(field);
            return wrapper;
        }

        var label = null;
        if (fieldDef.label) {
            label = renderLabel(fieldDef);
        }

        var field = null;
        if (fieldDef.data_type == 'file') {
            field = renderFileInput(fieldDef);
        }
        else {
            field = renderInput(fieldDef);
        }

        if (label) {
            wrapper.appendChild(label);
        }
        wrapper.appendChild(field);

        return wrapper;
    }

    function renderFieldList(fieldListDef, prefix, template) {
        var wrapper = document.createElement('div');

        var minEntries = fieldListDef.min_entries || 0;

        var fieldset = document.createElement('fieldset');
        fieldset.id = fieldListDef.id;
        fieldset.className = 'card';
        fieldset.setAttribute('data-value', '[]');
        fieldset.setAttribute('data-label', fieldListDef.field.label);
        fieldset.setAttribute('data-min-entries', minEntries);

        var header = renderFieldListHeader(fieldListDef);
        fieldset.appendChild(header);

        var body = document.createElement('div');
        body.className = 'card-body p-2 pb-0';

        var nav = renderFieldListNav(fieldListDef);
        body.appendChild(nav);

        var tabContent = renderFieldListTabs(fieldListDef, template);
        body.appendChild(tabContent);

        fieldset.appendChild(body);

        for (var i = 0; i < minEntries; i++) {
            addTabToFieldList(fieldset);
        }

        wrapper.appendChild(fieldset);
        return wrapper;
    }

    function renderFieldListHeader(fieldListDef) {
        var header = document.createElement('div');
        header.className = 'card-header d-flex';
        header.innerHTML = fieldListDef.label;

        var add = document.createElement('ul');
        add.className = 'nav ml-auto';

        var addLi = document.createElement('li');
        addLi.className = 'nav-item';

        var addBtn = document.createElement('a');
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

    function renderFieldListNav(fieldListDef) {
        var nav = document.createElement('nav');
        nav.className = 'mb-2';

        var pills = document.createElement('ul');
        pills.id = fieldListDef.id + '-pills';
        pills.className = 'nav nav-pills';

        var pillTemplate = document.createElement('li');
        pillTemplate.className = 'nav-item';
        pillTemplate.setAttribute('data-template', 'true');
        pillTemplate.style.display = 'none';

        var navBtn = document.createElement('a');
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

    function renderFieldListTabs(fieldListDef, template) {
        var tabContent = document.createElement('div');
        tabContent.id = fieldListDef.id + '-tabs';
        tabContent.className = 'tab-content';

        var tabTemplate = document.createElement('div');
        tabTemplate.id = fieldListDef.id + '-##-tab';
        tabTemplate.className = 'tab-pane pt-3 border-top';
        tabTemplate.style.display = 'none';
        tabTemplate.setAttribute('role', 'tabpanel');
        tabTemplate.setAttribute('aria-labelledby', fieldListDef.id + '-##-pill');
        tabTemplate.setAttribute('data-template', 'true');

        if (fieldListDef.field.data_type === 'form') {
            var formDef = fieldListDef.field.form_definition;
            var sep = fieldListDef.field.seperator || '_';

            tabTemplate.innerHTML = template.innerHTML;

            forms.draw(formDef, tabTemplate, fieldListDef.id + '-##' + sep)
        }
        else {
            var fieldDef = fieldListDef.field;
            var elem = forms.render(fieldDef, fieldListDef.id + '-##');
            if (elem) {
                tabTemplate.innerHTML = elem.outerHTML;
            }
        }

        var rem = document.createElement('div');
        rem.className = 'text-center';
        rem.style.display = 'none';

        var remBtn = document.createElement('a');
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

    function addTabToFieldList(fieldset) {
        var values = JSON.parse(fieldset.getAttribute('data-value'));
        var label = fieldset.getAttribute('data-label');
        var id = fieldset.id;

        var repl = new RegExp(id + '-##', 'g');
        var next = id + '-' + values.length;

        var nav = fieldset.querySelector('.nav.nav-pills'); 
        var pillTemplate = nav.querySelector('[data-template]');

        var old = nav.children;
        for (var i = 0, len = old.length; i < len; i++) {
            if (old[i].className.indexOf('nav-item') < 0) {
                continue;
            }
            var a = old[i].getElementsByTagName('a')[0];
            a.className = a.className.replace(' active', '');
        }

        var wrapper = document.createElement('div');
        wrapper.innerHTML = pillTemplate.outerHTML
            .replace(repl, next).replace(/#pillnum;/g, values.length + 1);

        var newPill = wrapper.children[0];
        newPill.removeAttribute('data-template');
        newPill.setAttribute('data-pill-id', values.length);
        newPill.style.display = '';
        newPill.getElementsByTagName('a')[0].className += ' active';
        nav.appendChild(newPill);

        var tabs = fieldset.querySelector('.tab-content');
        var tabTemplate = tabs.querySelector('[data-template]');

        old = tabs.children;
        for (var i = 0, len = old.length; i < len; i++) {
            if (old[i].className.indexOf('tab-pane') < 0) {
                continue;
            }
            old[i].className = old[i].className.replace(' show active', '');
        }

        var wrapper = document.createElement('div');
        wrapper.innerHTML = tabTemplate.outerHTML.replace(repl, next);

        var newTab = wrapper.children[0];
        newTab.removeAttribute('data-template');
        newTab.setAttribute('data-tab-id', values.length);
        newTab.className += ' show active';
        newTab.style.display = '';

        var remBtn = newTab.querySelector(
            '[data-fieldlist-rem][href="#remove-' + newTab.id + '"]');
        var minEntries = fieldset.getAttribute('data-min-entries');
        if (values.length >= parseInt(minEntries)) {
            remBtn.parentElement.style.display = '';
        }

        tabs.appendChild(newTab);


        values.push(1);
        fieldset.setAttribute('data-value', JSON.stringify(values));
    }

    function removeTabFromFieldList(fieldset, i) {
        var values = JSON.parse(fieldset.getAttribute('data-value'));

        var nav = fieldset.querySelector('.nav.nav-pills');
        nav.removeChild(nav.querySelector('[data-pill-id="' + i + '"]'));
        if (nav.children) {
            var targets = nav.children;
            for (var j = Math.min(i, targets.length - 1); j >= 0; j--) {
                if (targets[j].hasAttribute('data-template')) {
                    continue;
                }
                var a = targets[j].getElementsByTagName('a')[0];
                a.className += ' active';
                break;
            }
        }

        var tabs = fieldset.querySelector('.tab-content');
        tabs.removeChild(tabs.querySelector('[data-tab-id="' + i + '"]'));
        if (tabs.children) {
            var targets = tabs.children;
            for (var j = Math.min(i, targets.length - 1); j >= 0; j--) {
                if (targets[j].hasAttribute('data-template')) {
                    continue;
                }
                targets[j].className += ' show active';
                break;
            }
        }

        values.splice(i, 1);
        fieldset.setAttribute('data-value', JSON.stringify(values));
    }

    // Create a global event listener for adding to field lists
    document.body.addEventListener('click', function(e) {
        var btn = e.target.closest('a');
        if (btn == null || !btn.hasAttribute('data-fieldlist-add')) {
            return;
        }
        e.preventDefault();

        var fieldset = btn.closest('fieldset');
        addTabToFieldList(fieldset);
    });
    // Create a global event listener for removing from field lists
    document.body.addEventListener('click', function(e) {
        var btn = e.target.closest('a');
        if (btn == null || !btn.hasAttribute('data-fieldlist-rem')) {
            return;
        }
        e.preventDefault();

        var num = btn.closest('.tab-pane').getAttribute('data-tab-id');

        var fieldset = btn.closest('fieldset');
        removeTabFromFieldList(fieldset, parseInt(num));
    });

    function makeDependent(field_id, if_true, if_false, prefix) {
        if_true = if_true || [];
        if_false = if_false || [];
        prefix = prefix || '';

        if (!Array.isArray(if_true)) {
            if_true = [if_true];
        }
        if (!Array.isArray(if_false)) {
            if_false = [if_false];
        }

        if (!if_true && !if_false) {
            return;
        }

        for (var i = 0, len = if_true.length; i < len; i++) {
            if_true[i] = prefix + if_true[i];
        }
        for (var i = 0, len = if_false.length; i < len; i++) {
            if_false[i] = prefix + if_false[i];
        }

        function toggleVisible() {
            var field = document.getElementById(field_id);

            var group = field.closest('.form-group');
            group.style.display = '';

            for (var i = 0, len = if_true.length; i < len; i++) {
                var check = if_true[i];
                if (!document.getElementById(check).checked) {
                    group.style.display = 'none';
                    break;
                }
            }
            for (var i = 0, len = if_false.length; i < len; i++) {
                var check = if_false[i];
                if (document.getElementById(check).checked) {
                    group.style.display = 'none';
                    break;
                }
            }
        }

        document.body.addEventListener('change', function(e) {
            if (if_true.indexOf(e.target.id) < 0 &&
                if_false.indexOf(e.target.id) < 0) {
                return;
            }
            toggleVisible();
        });
        try {
            toggleVisible();
        }
        catch (e) {
            if (e instanceof TypeError) {
                // Assume the dom isn't fully loaded yet and try again
                setTimeout(toggleVisible, 50);
            }
            else {
                throw e;
            }
        }
    }

    forms.render = function(fieldDef, prefix, template) {
        fieldDef.id = (prefix || '') + (fieldDef.id || '');
        var group = document.createElement('div');
        group.className = 'form-group';

        if (fieldDef.data_type == 'field_list') {
            var wrapper = renderFieldList(fieldDef, prefix, template);
            group.innerHTML = wrapper.innerHTML;
        }
        else {
            var wrapper = renderSingleField(fieldDef);
            group.innerHTML = wrapper.innerHTML;

            var description = fieldDef.description;
            if (description) {
                var desc = document.createElement('small');
                small.className = 'form-text text-muted';
                small.innerHTML = description;
                group.appendChild(small);
            }
        }

        if (fieldDef.if_true || fieldDef.if_false) {
            makeDependent(
                fieldDef.id, fieldDef.if_true, fieldDef.if_false, prefix
            );
        }

        return group;
    };

    forms.draw = function(data, template, prefix) {
        if (!template.tagName.toLowerCase() == 'form' &&
            !template.hasAttribute('data-slot')) {
            return;
        }

        if (!template.hasAttribute('data-async-form')) {
            template.setAttribute('data-async-form', 'true');
        }

        if (data.table_id) {
            forms.drawTable(data, template, prefix);
        } 
        else {
            forms.drawForm(data, template, prefix);
        }
    }

    forms.drawForm = function(data, template, prefix) {
        var slotElements = template.querySelectorAll('[data-slot]');
        var slots = {};
        for (var i = 0, len = slotElements.length; i < len; i++) {
            var slot = slotElements[i]
            slots[slot.getAttribute('data-target')] = slot; 
        }

        var titleSlot = slots['title'];
        if (titleSlot) {
            titleSlot.innerHTML = data.title;
        }

        var fields = data.fields || [];
        for (var i = 0, len = fields.length; i < len; i++) {
            var f = fields[i];

            var slot = slots[f.id];
            if (slot) {
                if (f.data_type == 'form') {
                    forms.draw(f.form_definition, slot, f.id + (f.seperator || '_'));
                }
                else {
                    var elem = forms.render(f, prefix, slot);
                    if (elem) {
                        slot.outerHTML = elem.outerHTML;
                    }
                }
            }
        }
    };

    function getFields(form) {
        var fields = {};
        var inputs = ['input', 'select', 'textarea', 'fieldset'];
        for (var i = 0; i < inputs.length; i++) {
            fields[inputs[i] + 's'] = [].slice.call(
                form.getElementsByTagName(inputs[i])
            );
        }
        return fields
    }

    forms.populate = function(form, data) {
        // Convert data to an array if necessary
        // (helps us handle field-list/fieldsets)
        if (!Array.isArray(data)) {
            data = [data];
        }

        // Check if we need to build an id-prefix for field-list/fieldsets
        var pref = '';
        if (form.tagName.toLowerCase() == 'fieldset') {
            pref = form.id + '-';

            // Also check if we need to add tabs to the fieldset
            while (JSON.parse(form.getAttribute('data-value')).length < data.length) {
                addTabToFieldList(form);
            }
        }

        // Get available form fields
        var fields = getFields(form);

        for (var d = 0, dLen = data.length; d < dLen; d++) {
            var fullPref = pref === '' ? '' : pref + d + '_';
            var subData = data[d];

            // Fill in input fields
            for (var i = 0, len = fields.inputs.length; i < len; i++) {
                var input = fields.inputs[i];
                var checkId = input.id.replace(fullPref, '');
                if (subData[checkId] !== undefined) {
                    input.value = subData[checkId];
                }
            }

            // Fill in textarea fields
            for (var i = 0, len = fields.textareas.length; i < len; i++) {
                var textarea = fields.textareas[i];
                var checkId = textarea.id.replace(fullPref, '');
                if (subData[checkId] !== undefined) {
                    textarea.innerText = subData[checkId];
                }
            }

            // Fill in select fields
            for (var i = 0, len = fields.selects.length; i < len; i++) {
                var select = fields.selects[i];
                var checkId = select.id.replace(fullPref, '');
                if (subData[checkId] !== undefined) {
                    select.selectedIndex = -1;
                    var opts = select.children;
                    for (var j = 0; j < opts.length; j++) {
                        if (opts[j].value == subData[checkId]) {
                            select.selectedIndex = j;
                            break;
                        }
                    }
                }
            }

            // Fill in fieldsets
            for (var i = 0, len = fields.fieldsets.length; i < len; i++) {
                var fieldset = fields.fieldsets[i];
                var checkId = fieldset.id.replace(fullPref, '');
                if (subData[checkId] !== undefined) {
                    forms.populate(fieldset, subData[checkId])
                }
            }
        }
    };

    forms.drawTable = function(data, template, prefix) {
        let tableSlot = document.querySelector('#'+data.table_id);
        if (data.pivot) {
            tableSlot.innerHTML += data.header;

            let tbody = create_element('tbody', tableSlot);
            let fields = data.fields || [];
            for (var i = 0, len = fields.length; i < len; i++) {  
                let tr = create_element('tr', tbody);        
                let td = create_element('td', tr)
                forms.renderTableHeader(fields[i], td);
            }
        }
        else {
            let thead = create_element('thead', tableSlot);
            let tr = create_element('tr', thead);
            let fields = data.fields || [];
            for (var i = 0, len = fields.length; i < len; i++) {          
                let th = create_element('th', tr)
                forms.renderTableHeader(fields[i], th);
            }
        }
    };

    // TODO: Need to remove embedded HTML in help text
    forms.renderTableHeader = function(fieldDef, th) {
        let labelId = fieldDef.id;
        if (typeof labelId !== 'string' && !(labelId instanceof String)) {
            labelId = JSON.stringify(fieldDef.id);
        }
        let labelText = fieldDef.label;
        let tooltip = fieldDef.tooltip;
        let default_val = JSON.stringify(fieldDef.default);
        let help = fieldDef.help;

        let label = create_element("label", th);
        label.innerHTML = labelText;
        label.setAttribute('data-id', labelId);
        label.setAttribute('data-default', default_val);

        label.setAttribute('data-toggle', 'tooltip');
        label.setAttribute('data-placement', 'auto');
        label.setAttribute('data-html', 'true');
        if (tooltip) {
            label.title = "";
            label.setAttribute('data-original-title', tooltip);
        }
        if (help) {
            forms.renderTableHelp(help, labelText, th)
        }
        return label;
    }

    forms.renderTableHelp = function(note, title, node){
        let marker = create_element("sup", node);

        let toggle = create_element("a", marker);
        toggle.href = 'javascript:void(0);';
        toggle.setAttribute('data-toggle', 'popover');
        toggle.setAttribute('data-original-title', title);
        toggle.setAttribute('data-content', note);

        let symbol = create_element("i", toggle);
        symbol.className = 'fa fa-question';
    }

    // Helper method
    function create_element(EleToCreate, parent) {
        let child = document.createElement(EleToCreate);
        return parent.appendChild(child);
    }

    // Grab default value stuck in column header
    forms.fetchDefault = function(id){
        let ele = $('[data-id="'+id+'"]')[0];
        let val = ele.getAttribute("data-default");
        return JSON.parse(val);
    }

    // On dom load, auto-draw forms that are labelled async
    var formLoadEvent = document.createEvent('Event');
    formLoadEvent.initEvent('form:loaded', true, true);
    document.addEventListener("DOMContentLoaded", function(e) {
        var formTemplates = document.getElementsByTagName('form');
        for (var i = 0, len = formTemplates.length; i < len; i++) {
            var template = formTemplates[i];
            if (!template.getAttribute('data-async-form')) {
                continue;
            }
            var src = template.getAttribute('data-form-src')
            if (!src) {
                continue;
            }
            loadAsyncForm(template, src);
        }
    });
    function loadAsyncForm(template, src) {
        LoadingScreen.show(src);
        TRIM.api.loadForms(src).on('load', function() {
            try {
                var data = this.responseJSON;
                if (data && data[src]) {
                    forms.draw(data[src], template);
                    template.className = template.className + ' form-loaded';
                    template.dispatchEvent(formLoadEvent);
                }
            }
            finally {
                LoadingScreen.hide(src);
            }
        });
    }

    trim.forms = forms;
    return trim;
})(window.TRIM || {});
