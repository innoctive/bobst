function handlespecialchars(input) {
        var inputvalue = input.value
        var newvalue = inputvalue.split("&").join("and");
        newvalue = newvalue.split("#").join(" ");
        newvalue = newvalue.split("'").join("");
        document.getElementById(input.id).value = newvalue;
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function titleCase(str) {
  return str.toLowerCase().split(' ').map(function(word) {
    return (word.charAt(0).toUpperCase() + word.slice(1));
  }).join(' ');
}
