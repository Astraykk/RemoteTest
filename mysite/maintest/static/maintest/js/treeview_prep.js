var List = {{ List|safe }};
var Dict = {{ Dict|safe }};

document.getElementById("demo").innerHTML={{ List|safe }}
//document.getElementById("demo").innerHTML= Dict

