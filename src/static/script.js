"use strict";


function submitForm(form)
{
    var xhr = new XMLHttpRequest();
    xhr.onload = function(){ alert (xhr.responseText); }
    xhr.onerror = function(){ alert (xhr.responseText); }
    xhr.open(form.method, "/insert/happiness", true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    var data = new FormData(form)

    // append date
    var current_day = window.location.href.split("/day/")[1];  // that's questionable
    data.append("date", current_day)

    console.log(data)
    xhr.send(data);
    return false;
}