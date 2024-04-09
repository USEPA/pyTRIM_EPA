function isNumber(str) {
    const numberRegex = /^\s*[+-]?(\d+|\d*\.\d+|\d+\.\d*)([Ee][+-]?\d+)?\s*$/
    return numberRegex.test(str)
}

function ErrToolTip(ele, is_valid, message) {
    let parent = $(ele).parent();
    $(parent).find("label.warningTT").tooltip('dispose');
    $(parent).find("label.warningTT").remove();

    if (!is_valid) {
        let tt = '<label class="warningTT" data-toggle="tooltip" data-placement="top" data-html="true" title="'+message+'"><i class="ml-1 fas fa-exclamation-triangle"></i></label>';
        let this_cell = $(ele).closest("td");
        if (this_cell.length > 0) {
            $("label.warningTT").tooltip('hide');
            $(this_cell).append(tt);
            $(this_cell).find("label.warningTT").tooltip('show');
        } else {
            let this_txt = $(ele).closest("div");
            $("label.warningTT").tooltip('hide');
            $(this_txt).prepend(tt);
            $(this_txt).find("label.warningTT").tooltip('show');
        }

    }
    return is_valid
}

function elementIsValid(ele){
    return $(ele).find(".warningTT").length === 0;
}

// Table error validation
let ErrorValidation = {
    isPositiveValue : function (ele) {
        if (!this.isValidNumber(ele)) {
            return false;
        }
        let data = $(ele).val();
        let is_valid = parseFloat(data) >= 0;
        return ErrToolTip(ele, is_valid, "Value must be positive.");
    },
    isValidNumber : function (ele) {
        let data = $(ele).val();
        let is_valid = isNumber(data);
        return ErrToolTip(ele, is_valid, "Invalid values found within number.");
    },
    rowTotalIsValid : function (ele) {
        let row = ele.closest("tr");
        let cells = $(row).find("input.editableCell");
        let expected_total = parseFloat($(row).data("rsval"));
        let total = cells.toArray().reduce((ps,e) => ps + parseFloat($(e).val()),0);

        let is_valid = total === expected_total;
        ele = $(ele).closest("td")
        return ErrToolTip(ele, is_valid, "Sum of the fractions for given consuming organism should be "+expected_total)
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
    }
}
