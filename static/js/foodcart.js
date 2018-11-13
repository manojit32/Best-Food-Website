
function loadDoc(url, cFunction) {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            cFunction(this);
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

function postJSON(url, jsonObject) {
    console.log("im in d");

    console.log("post started")
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(jsonObject));
    //xhttp.send("u_cart="+JSON.stringify(jsonObject));
    console.log("Sending ..." + "u_cart=" + JSON.stringify(jsonObject))
    console.log("post completed2")
    xhttp.onload = function () {
        // Do whatever with response
        //alert(xhttp.responseText);
        loadDoc("/homepage", function(){alert("Successfully posted menu")})
    }
    console.log("post completed3")
    // }
}



//localStorage.removeItem('dataObject');

function trim(s){ 
  return ( s || '' ).replace( /^\s+|\s+$/g, '' ); 
}
var email=document.querySelector("[data-useremail]").innerText.trim();
email = trim(email)
console.log("$$$"+'dataObject'+email+"$$$");

retrievedObject = localStorage.getItem('dataObject'+email);
if (!(retrievedObject === null)) {
    b_cart = JSON.parse(retrievedObject);
    console.log(b_cart)
    //b_cart.forEach(function(restaurant){
    //restaurant.forEach(function(item){
    //console.log(restaurant + ":" + item);
    //console.log(item.value+"---------------")
    //document.getElementById(restaurant+":"+item).value=item.value;
    //})
    //});
    
    for (var restaurant in b_cart) {
        for (var item in b_cart[restaurant]) {
            console.log(restaurant + ":" + item);
            console.log(b_cart[restaurant][item] + "---------------");
            //document.getElementById(restaurant + ':' + item).value = b_cart[restaurant][item];
            
          
            try {
                d=document.querySelectorAll('[data-riid="' + restaurant + ':' + item + '"]')
                d[0].value =b_cart[restaurant][item]
                //var d1=document.querySelector('[data-icard="' + restaurant + ':' + item + '"]').outerHTML

                
            }
            catch (e) {

            }
        }
        //*[@id="1"]
    }

    

}
else {
    b_cart = {};
}


function inc(obj) {
    var id = obj.value;
    var value = parseInt(document.getElementById(id).value);

    if(addItemToCart(obj, ++value)==true)
    {
    document.getElementById(id).value = value;

}
    try{
        console.log("hero"+"#order > #".concat(id))
        var a= "#\\3"+id
        // document.querySelectorAll("#\\32")[0]
        console.log(document.querySelectorAll(a)[1])
        document.querySelectorAll(a)[1].value = value;
        console.log("hello")

        // console.log("hello"+document.getElementById("order").getElementById(id).value)
    }
    catch(e){

    }
   
   
    
    reloadSidebar();
}
function dec(obj) {
    var id = obj.value;
    var value = parseInt(document.getElementById(id).value);
    if (value > 0) {
        document.getElementById(id).value = --value;
         try{
        console.log("hero"+"#order > #".concat(id))
        var a= "#\\3"+id
        // document.querySelectorAll("#\\32")[0]
        console.log(document.querySelectorAll(a)[1])
        document.querySelectorAll(a)[1].value = value;
        console.log("hello")
        if(value==0)
        {
            var b=findAncestor(document.querySelectorAll(a)[1],"card")
        b.outerHTML=null;

          
        }
        // console.log("hello"+document.getElementById("order").getElementById(id).value)
    }
    catch(e){

    }



    }
    else {
        value = 0;
        var a= "#\\3"+id
        


    }

    
    addItemToCart(obj, document.getElementById(id).value);
    reloadSidebar();
}

function findAncestor (el, cls) {
   while ((el = el.parentElement) && !el.classList.contains(cls));
   return el;
}




function addItemToCart(obj, val) {
    var r_id = obj.getAttribute("data-r_id");
    var i_id = obj.getAttribute("data-i_id");
    console.log(r_id + " " + i_id)

    if (r_id in b_cart) {

        console.log(r_id)
        if(val!=0){
        b_cart[r_id][i_id] = val}
        if (val == 0) {
            delete b_cart[r_id][i_id];
            if (Object.keys(b_cart[r_id]).length == 0) {
                delete b_cart[r_id];
            }
        }
        localStorage.setItem('dataObject'+email, JSON.stringify(b_cart));
    console.log(localStorage.getItem("dataObject"+email))
        return true;
    }
    else {
           
           var count = Object.keys(b_cart).length;
            console.log(count);
        if(count>0)
        {
            alert("you have items from another restaurant");
             var r=confirm('Do you Want to Clear Cart and add these items?'); if(r==true)
              {
                var temp_rid=Object.keys(b_cart)[0];
                //document.querySelectorAll()
                var old_rest_value_buttons = document.querySelectorAll("[data-riid*='"+temp_rid+":']");
                console.log("bugg"+old_rest_value_buttons)
                for (var button of old_rest_value_buttons){
                    button.value = "0";
                    console.log("im innnnnnnnnnnnnnnnnn"+button)
                }
                localStorage.removeItem('dataObject'+email);

                b_cart={};
                 b_cart[r_id] = {};
                 b_cart[r_id][i_id] = val;
                 localStorage.setItem('dataObject'+email, JSON.stringify(b_cart));
              console.log(localStorage.getItem("dataObject"+email))

                 return true;
               
              }
              else
              {
                localStorage.setItem('dataObject'+email, JSON.stringify(b_cart));
    console.log(localStorage.getItem("dataObject"+email))
                return false;
              }

        }
        //alert("you have items form another restaurant");
        
        //var r=confirm('Do you Want to Clear Cart?'); if(r==true){localStorage.removeItem('dataObject');alert('cart cleared');location.reload();}
        else 
        {
            if(val>0){
            b_cart[r_id] = {}
            b_cart[r_id][i_id] = val
            localStorage.setItem('dataObject'+email, JSON.stringify(b_cart));
    console.log(localStorage.getItem("dataObject"+email))
            return true;
            }
            return false;

        }
    }
}
function reloadSidebar()
{

    // retrievedObject2 = localStorage.getItem('dataObjectCart' + email);
    // if (!(retrievedObject2 === null)) {
    //     SBHTML = retrievedObject2;
    //     // alert(SBHTML);
    //     document.getElementById("order").innerHTML = "<pre>"+SBHTML+"</pre>";
    //     if (document.getElementById("chkout") == undefined) {
    //         document.getElementById("order").insertAdjacentHTML("afterend", '<button type="button" id="chkout" class="btn btn-primary"  onclick="checkout();">\
    //     Check out\
    // </button>');
    //     }
    // }

    // else {
    //     SBHTML = "";
    // }


retrievedObject = localStorage.getItem('dataObject'+email);
if (!(retrievedObject === null)) {
    b_cart = JSON.parse(retrievedObject);
    console.log(b_cart)
    //b_cart.forEach(function(restaurant){
    //restaurant.forEach(function(item){
    //console.log(restaurant + ":" + item);
    //console.log(item.value+"---------------")
    //document.getElementById(restaurant+":"+item).value=item.value;
    //})
    //});
    var d="";
    for (var restaurant in b_cart) {
        for (var item in b_cart[restaurant]) {
            console.log(restaurant + ":" + item);
            console.log(b_cart[restaurant][item] + "---------------");
            //document.getElementById(restaurant + ':' + item).value = b_cart[restaurant][item];
            
            try {
                // document.querySelector('[data-riid="' + restaurant + ':' + item + '"]').value = b_cart[restaurant][item];
                var d2=document.querySelectorAll('[data-riid="' + restaurant + ':' + item + '"]')
                // for(item in d2)
                // {
                //                  console.log(item)

                //     //item.value=b_cart[restaurant][item];
                // }
               var d1=document.querySelector('[data-icard="' + restaurant + ':' + item + '"]').outerHTML

               d=d+d1;



            }
            catch (e) {
            
            }
        }
        //*[@id="1"]
    }

    
    if(d!="")
    {   
        document.getElementById("order").innerHTML = d;
        if (document.getElementById("chkout") == undefined){
        document.getElementById("order").insertAdjacentHTML("afterbegin",'<button type="button" id="chkout" class="btn btn-primary pull-right"  onclick="checkout();">\
        Check out\
    </button>');
    }
        // localStorage.setItem('dataObjectCart' + email, d);
    }

    else {
        document.getElementById("order").innerHTML = "";
        // localStorage.removeItem('dataObjectCart' + email);
    }


 

}
else {
    b_cart = {};
}

}

function checkout() {
    retrievedObject = localStorage.getItem('dataObject'+email);
    if (!(retrievedObject === null)) {

        b_cart = JSON.parse(retrievedObject);
        checkoutOrder("/checkout", b_cart);

    }
    else {
        b_cart = {}
        alert("Please Add Some Items To Cart");
    }
}

function checkoutOrder(url, jsonObject) {
    console.log("im in d");

    // if (jsonObject.length>0){
    console.log("post started")
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.open("POST", url, true)
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    //xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
    console.log("post completed1")
    xhttp.send(JSON.stringify(jsonObject));
    //xhttp.send("u_cart="+JSON.stringify(jsonObject));
    console.log("Sending ..." + "u_cart=" + JSON.stringify(jsonObject))
    console.log("post completed2")
    xhttp.onload = function () {
        // Do whatever with response
        //alert(xhttp.responseText);
        loadDoc("/getcheckoutform", loadCheckOutForm)
    }
    //xhttp.onloadend = loadDoc("/getcheckoutform", loadCheckOutForm)
    console.log("post completed3")
    // }
}


function loadCheckOutForm(x) {
    console.log("Im in checkoutform" + x.responseText)
    document.querySelector(".container-fluid").innerHTML = x.responseText;
}


function clearCart(){
    localStorage.removeItem('dataObject{{session.email}}');
    document.write("Cart cleared using JS");
}