
    function checkForm(form)
  {
    if(form.u_name.value == "") {
        alert("Error: Username cannot be blank!");
    form.u_name.focus();
    return false;
  }
      re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(!re.test(form.u_name.value)) {
        alert("Error: Username must contain only letters, numbers and @");
    form.u_name.focus();
    return false;
  }

    if(form.u_password.value != "" && form.u_password.value == form.u_c_password.value) {
      if(form.u_password.value.length < 6) {
        alert("Error: Password must contain at least six characters!");
    form.u_password.focus();
    return false;
  }
      if(form.u_password.value == form.u_name.value) {
        alert("Error: Password must be different from Username!");
    form.u_password.focus();
    return false;
  }
  re = /[0-9]/;
      if(!re.test(form.u_password.value)) {
        alert("Error: password must contain at least one number (0-9)!");
    form.u_password.focus();
    return false;
  }
  re = /[a-z]/;
      if(!re.test(form.u_password.value)) {
        alert("Error: password must contain at least one lowercase letter (a-z)!");
    form.u_password.focus();
    return false;
  }
  re = /[A-Z]/;
      if(!re.test(form.u_password.value)) {
        alert("Error: password must contain at least one uppercase letter (A-Z)!");
    form.u_password.focus();
    return false;
  }
    } else {
        alert("Error: Please check that you've entered and confirmed passwords are same!");
    form.u_password.focus();
    return false;
  }

  //alert("You entered a valid password: " + form.u_password.value);
  return true;
}
