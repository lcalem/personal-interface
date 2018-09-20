"use strict";

function convertDate(date) 
{
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString();
    var dd  = date.getDate().toString();

    var mmChars = mm.split('');
    var ddChars = dd.split('');

    return yyyy + '-' + (mmChars[1] ? mm : "0" + mmChars[0]) + '-' + (ddChars[1] ? dd : "0" + ddChars[0]);
}


function submitForm(form)
{
    var xhr = new XMLHttpRequest();
    xhr.onload = function(){ alert (xhr.responseText); }
    xhr.onerror = function(){ alert (xhr.responseText); }
    xhr.open(form.method, "/insert/happiness", true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    var data = new FormData(form)

    // append date
    var today = new Date();
    data.append("date", convertDate(today))

    console.log(data)
    xhr.send(data);
    return false;
}