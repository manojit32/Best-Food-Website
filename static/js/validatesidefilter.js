function validateDecimal(value) {
    var RE = /^\d*(\.\d{1})?\d{0,1}$/;
    if (RE.test(value)) {
        return true;
    } else {
        return false;
    }
}

function checksideFilter(form) {
    // if (form.u_name.value == "") {
    //     alert("Error: Username cannot be blank!");
    //     form.u_name.focus();
    //     return false;
    // }
    var minp = validateDecimal(form.minprice.value);
    var maxp = validateDecimal(form.maxprice.value);
    if (!minp) {
        alert("Error: " + form.minprice.value+" is not a integer/double-precision float");
        form.minprice.focus();
        return false;
    }
    if (!maxp) {
        alert("Error: " + form.maxprice.value + " is not a integer/double-precision float");
        form.maxprice.focus();
        return false;
    }
    if (parseFloat(form.minprice.value) > parseFloat(form.maxprice.value)) {
        alert("Error: minprice " + form.minprice.value + "cannot be greater than maxprice"+form.maxprice.value);
        form.minprice.focus();
        return false;
    }

    // if (form.u_password.value != "" && form.u_password.value == form.u_c_password.value) {
    //     if (form.u_password.value.length < 6) {
    //         alert("Error: Password must contain at least six characters!");
    //         form.u_password.focus();
    //         return false;
    //     }
    //     if (form.u_password.value == form.u_name.value) {
    //         alert("Error: Password must be different from Username!");
    //         form.u_password.focus();
    //         return false;
    //     }
    //     re = /[0-9]/;
    //     if (!re.test(form.u_password.value)) {
    //         alert("Error: password must contain at least one number (0-9)!");
    //         form.u_password.focus();
    //         return false;
    //     }
    //     re = /[a-z]/;
    //     if (!re.test(form.u_password.value)) {
    //         alert("Error: password must contain at least one lowercase letter (a-z)!");
    //         form.u_password.focus();
    //         return false;
    //     }
    //     re = /[A-Z]/;
    //     if (!re.test(form.u_password.value)) {
    //         alert("Error: password must contain at least one uppercase letter (A-Z)!");
    //         form.u_password.focus();
    //         return false;
    //     }
    // } else {
    //     alert("Error: Please check that you've entered and confirmed your password!");
    //     form.u_password.focus();
    //     return false;
    // }

    // alert("You entered a valid password: " + form.u_password.value);
    return true;
}