function jsonToHtml(json, papai) {
    json.map(function (obj) {
        var divobj = document.createElement("div");
        for (var att in obj) {
            if (att == "innerHTML") {
                divobj.innerHTML = obj[att];
            } else if (att != "filho") {
                divobj.setAttribute(att, obj[att]);
            }
        }
        papai.appendChild(divobj);
        if (typeof (obj.filho) == "object") {
            jsonToHtml(obj.filho, divobj);
        }
    })
}

function parseTime(total, interval, chronoObj) {
    total -= 1000;
    var diff = total;
    if (total < 0) {
        clearInterval(interval);
        total = 0;
    }
    var days = total / (24 * 3600 * 1000);
    total %= (24 * 3600 * 1000);
    var hours = (total / 3600000)
    total %= 3600000
    var minutes = (total / 60000)
    total %= 60000
    var seconds = (total / 1000)
    total %= 1000
    //console.log(interval);
    chronoObj["d"].innerHTML = Math.floor(days);
    chronoObj["h"].innerHTML = Math.floor(hours);
    chronoObj["m"].innerHTML = Math.floor(minutes);
    chronoObj["s"].innerHTML = Math.floor(seconds);
    return diff;
}

function start(dataAtual, dataLimite, interval, chronoObj) {
    var diff = dataLimite.getTime() - dataAtual.getTime();
    //console.log("Lim "+dataLimite+"\n"+"atual "+dataAtual)
    diff = parseTime(diff, interval, chronoObj);
    interval.value = setInterval(function () {
        diff = parseTime(diff, interval, chronoObj);
        if(diff <= 0){
            clearInterval(interval.value);
            chronoObj["title"].innerHTML = "A contagem terminou! O evento já começou!"
            chronoObj["title"].style.fontSize = "1.3em";
        }
    }, 1000);
}
//Data( year, day, hour, minute, seconds, millis)
function addchronos(year, month, day, hours, minutes, seconds) {
    var chronos = document.getElementById('chronos');
    var divs = [{"id":"titleChronos","innerHTML":""},{"id":"blockChronos","filho":[{"class":"block_num","filho":[{"class":"number","id":"days"},{"class":"desc","innerHTML":"Dias"}]},{"class":"block_num","filho":[{"class":"number","id":"hours"},{"class":"desc","innerHTML":"Horas"}]},{"class":"block_num","filho":[{"class":"number","id":"minutes"},{"class":"desc","innerHTML":"Minutos"}]},{"class":"block_num","filho":[{"class":"number","id":"seconds"},{"class":"desc","innerHTML":"Segundos"}]}]}];
    jsonToHtml(divs, chronos);

    var dataLimite = new Date(year, month, day, hours, minutes, seconds, 0);
    var dataAtual = new Date();
    var chronoObj = {
        "h": document.getElementById("hours"),
        "d": document.getElementById("days"),
        "m": document.getElementById("minutes"),
        "s": document.getElementById("seconds"),
        "block": document.getElementById("blockChronos"),
        "title": document.getElementById("titleChronos")
    }
    var interval = {
        value: null
    };
    var diff = 0;
    start(dataAtual, dataLimite, interval, chronoObj);

    //Adiquirindo a hora certa e atualizando a dataAtual
    var xml = new XMLHttpRequest();
    var url = "https://script.google.com/macros/s/AKfycbyd5AcbAnWi2Yn0xhFRbyzS4qMq1VucMVgVvhul5XqS9HkAyJY/exec?tz=America/Fortaleza";
    xml.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var fortjson = JSON.parse(this.response);
            //console.log(fortjson);
            dataAtual = new Date(fortjson.year, fortjson.month - 1, fortjson.day, fortjson.hours, fortjson.minutes, fortjson.seconds, fortjson.millis);
            clearInterval(interval.value);
            //console.log("chegou "+dataAtual+"  "+fortjson.month)
            start(dataAtual, dataLimite, interval, chronoObj);
        }
    }
    xml.open("GET", url, true);
    xml.send();
}
