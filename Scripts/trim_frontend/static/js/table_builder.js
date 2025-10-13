function isNumber(str) {
    const numberRegex = /^\s*[+-]?(\d+|\d*\.\d+|\d+\.\d*)([Ee][+-]?\d+)?\s*$/
    return numberRegex.test(str)
}

function standardize_val(val) {
    // standardize value e.g. '.5' -> '0.5'
    let standardized_val = Number(val).toString();
    if (!standardized_val.includes('.')) {
        standardized_val += '.0';
    }
    return standardized_val // string
}

function scientific(val) { // to scientific notation
    return new Intl.NumberFormat('en-US', {notation: "scientific"}).format(parseFloat(val));
}

// static value dropdown menu of column names
function appendHeaderOptions(datatable, skip_columns=[]) {
    // clear existing options to avoid duplicates
    $("#" + datatable.attr('id') + "_columns").empty();
    datatable.api().columns().every(function(column_idx) {
        let header = this.header().textContent;
        if (!skip_columns.includes(header))
            $("#"+datatable.attr('id')+"_columns").append(`<option value='${column_idx}'>${header}</option>`);
    })
}

function ErrToolTip(ele, is_valid, message, parent_ele="td") {
    let parent = $(ele).parent();
    $(parent).find("label.warningTT").tooltip('dispose');
    $(parent).find("label.warningTT").remove();

    if (!is_valid) {
        let tt = '<label class="warningTT" data-toggle="tooltip" data-placement="top" data-html="true" title="'+message+'"><i class="ml-1 fas fa-exclamation-triangle"></i></label>';
        let this_cell = $(ele).closest(parent_ele);
        if (this_cell.length > 0) {
            $("label.warningTT").tooltip('hide');
            $(this_cell).append(tt);
            $(this_cell).find("label.warningTT").tooltip('show').tooltip('hide');
        } else {
            let this_txt = $(ele).closest("div");
            $("label.warningTT").tooltip('hide');
            $(this_txt).prepend(tt);
            $(this_txt).find("label.warningTT").tooltip('show').tooltip('hide');
        }

    }
    return is_valid
}

function elementIsValid(ele){
    return $(ele).find(".warningTT").length === 0;
}

// Table error validation
let ErrorValidation = {
    isPositiveValue : function (ele, parent_ele="td") {
        if (!this.isValidNumber(ele)) {
            return false;
        }
        let data = $(ele).val();
        let is_valid = parseFloat(data) >= 0;
        return ErrToolTip(ele, is_valid, "Value must be positive.", parent_ele);
    },
    isValidNumber : function (ele, parent_ele="td") {
        let data = $(ele).val();
        let is_valid = isNumber(data);
        return ErrToolTip(ele, is_valid, "Invalid values found within number.", parent_ele);
    },
    isWithinRange : function (ele, parent_ele="td", min=undefined, max=undefined) {
        if (!this.isValidNumber(ele)) {
            return false;
        }
        let data = $(ele).val();
        let is_valid = parseFloat(data);
        let msg = "Value is not valid.";

        if (min !== undefined && max !== undefined) {
            is_valid = (is_valid >= min && is_valid <= max);
            msg = `Value must be between, or equal to, ${min} and ${max}.`;
        }
        else if (min !== undefined) {
            is_valid = is_valid >= min;
            if (min == Number.MIN_VALUE)
                msg = `Value must be greater than 0.`;
            else
                msg = `Value must be greater than or equal to ${min}.`;
        }
        else if (max !== undefined) {
            is_valid = is_valid <= max;
            msg = `Value must be less than or equal to ${max}.`;
        }

        return ErrToolTip(ele, is_valid, msg, parent_ele);
    },
    rowTotalIsValid : function (ele) {
        let row = ele.closest("tr");
        let cells = $(row).find("input.editableCell");
        let expected_total = parseFloat($(row).data("rsval"));
        let message_entity = $(row).data("entity") || "fractions for given consuming organism"
        let total = cells.toArray().reduce((ps,e) => ps + parseFloat($(e).val()),0).toFixed(4);  // exact comparison may not be possible due to precision so compare using less precise total

        let is_valid = total == expected_total;
        ele = $(ele).closest("td")
        return ErrToolTip(ele, is_valid, `Sum of the ${message_entity} should be ${expected_total}, but the total is ${total}`)
    },
    rowTotalIsLessOrEqual : function (ele) {
        let row = ele.closest("tr");
        let cells = $(row).find("input.editableCell");
        let expected_total = parseFloat($(row).data("rsval"));
        let message_entity = $(row).data("entity") || "fractions for given consuming organism"
        let total = cells.toArray().reduce((ps,e) => ps + parseFloat($(e).val()),0).toFixed(4);  // exact comparison may not be possible due to precision so compare using less precise total

        let is_valid = total <= expected_total;
        ele = $(ele).closest("td")
        return ErrToolTip(ele, is_valid, `Sum of the ${message_entity} should be ${expected_total}, but the total is ${total}`)
    },
    isValidFraction : function (ele) {
        if (!this.isPositiveValue(ele)) {
            return false;
        }
        let data = $(ele).val();
        let is_valid = parseFloat(data) <= 1;
        return ErrToolTip(ele, is_valid, "Fractional value must be no greater than 1.");
    },
    isInSimulationTimeSpan: function(ele, datedata){
        let has_data = datedata.length > 0;
        return ErrToolTip(ele, has_data, "Input date(s) not in simulation date range.")
    },
    fileHasData: function(ele, filedata){
        let has_data = filedata.length > 0;
        return ErrToolTip(ele, has_data, "Input file has no data.")
    },
    fileIsParsed: function(ele, has_data) {
        let fileIsParsed = has_data
        return ErrToolTip(ele, fileIsParsed, "CSV file parse problem")
    },
    tsFileHasDateColumn: function (ele, tsData){
        let has_data = false
        if (tsData) {
            has_data = tsData.length > 0;
        } else {
            this.fileIsParsed(ele, has_data)
            return
        }

        if (has_data) {
            let has_date_col = Object.keys(tsData[0]).indexOf("Date") > -1
            return ErrToolTip(ele, has_date_col, "Input time-series file has no column with name 'Date'")
        } else {
            this.fileHasData(ele, tsData)
        }
    }

}
