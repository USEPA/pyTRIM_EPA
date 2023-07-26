/*
Move more generic table stuff in here eventually ...
*/

// Table error validation
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
        $("label.warningTT").tooltip('hide');
        $(this_cell).append(tt);
        $(this_cell).find("label.warningTT").tooltip('show');
    }
    return is_valid
}

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
    }
}
