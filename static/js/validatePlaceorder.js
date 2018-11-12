function validatePhoneNumber(obj){
   alert(obj);
   for (var i=0;obj.length();i++){
       if (! (Integer(obj[i]) in [0,1,2,3,4,5,6,7,8,9])){
           alert(obj[i]);
            return false;    
       }
       alert("true");
   }
    return true;
    }
function checkUserForm(form) {
    console.log(form);
    alert("It here!!");
    if (form.u_name.value=="''"){
        alert("Error: Username cannot be ''");
    form.u_name.focus();
    return false;
    } 
    alert("2");
    if(form.u_name.value == "") {
        alert("Error: Username cannot be blank!");
    form.u_name.focus();
    return false;
    }
    alert("3");
    if(!validatePhoneNumber(form.u_phone.value.toString())){
    alert("Error: Number should be of length 10 and needs to begin with either 7,8 or 9!");
    form.u_phone.focus()
    return false;
    }
    alert("4")
    return true;
}