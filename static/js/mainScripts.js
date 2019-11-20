function validateForm(formName, type){

buildString = "<p>Please fix the following errors before proceeding:</p>"
console.log(document.forms[formName][type+'Age'].value)
var valid = true

if (document.forms[formName][type+'Name'].value == "" || document.forms[formName][type+'Age'].value == "" || document.forms[formName][type+'Balance'].value == "" || document.forms[formName][type+'Email'].value == "" || document.forms[formName][type+'Address'].value == ""){
    buildString = buildString + "<p>All fields must contain a value</p>"
  valid = false
}

if (document.forms[formName][type+'Age'].value <= 0){
  buildString = buildString + "<p>Age must be greater than zero</p>"
}

if(isNaN(document.forms[formName][type+'Age'].value)){
  buildString = buildString + "<p>Age must be a valid number</p>"
}

if(isNaN(document.forms[formName][type+'Balance'].value)){
  buildString = buildString + "<p>Balance must be a valid number</p>"
}

if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.forms[formName][type+'Email'].value) == false){
  buildString = buildString + "<p>Please enter a valid email address</p>"
  valid = false
}

if (valid == false){
  document.getElementById('validationResponse').innerHTML = buildString;
}
return valid
}

(function() {
// variable to store our current state
var cbstate;

// bind to the onload event
window.addEventListener('load', function() {
  // Get the current state from localstorage
  // State is stored as a JSON string
  cbstate = JSON.parse(localStorage['CBState'] || '{}');

  // Loop through state array and restore checked
  // state for matching elements
  for(var i in cbstate) {
    var el = document.querySelector('input[name="' + i + '"]');
    if (el) el.checked = true;
  }

  // Get all checkboxes that you want to monitor state for
  var cb = document.getElementsByClassName('save-cb-state');

  // Loop through results and ...
  for(var i = 0; i < cb.length; i++) {

    //bind click event handler
    cb[i].addEventListener('click', function(evt) {
      // If checkboxe is checked then save to state
      if (this.checked) {
        cbstate[this.name] = true;
      }

  // Else remove from state
      else if (cbstate[this.name]) {
        delete cbstate[this.name];
      }

  // Persist state
      localStorage.CBState = JSON.stringify(cbstate);
    });
  }
});
})();