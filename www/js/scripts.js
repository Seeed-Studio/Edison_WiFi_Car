
function forward()
{
    send('w');
}
function turn_left()
{
    send('a');
}
function stop()
{
    send('z');
}
function turn_right()
{
    send('d')
}
function backward()
{
    send('s');
}

var keyPressed = false;
function init()
{
    if (document.addEventListener) {
        document.addEventListener("keydown", keydown, false);
        document.addEventListener("keyup", keyup, false);
        document.addEventListener("keypress", keypress, false);
    } else if (document.attachEvent) {
        document.attachEvent("onkeydown", keydown);
        document.attachEvent("onkeyup", keyup);
        document.attachEvent("onkeypress", keypress);
    } else {
        document.onkeydown = keydown;
        document.onkeyup = keyup;
    }
}

function keydown(e)
{
    var chars = ['w', 'a', 's', 'd', 'e', 'c', 'z', 'a', 'w', 'd', 's', 'i', 'j', 'k', 'l', 'o'];
    var codes = [ 87,  65,  83,  68,  69,  67,  90,  37,  38,  39,  40,  73,  74,  75,  76,  79];
    <!-- 37 left; 38 up; 39 right; 40 down; -->
    var code;

    if (keyPressed) {
        return;
    }
    keyPressed = true;

    e = e ? e : event;
    code = e.keyCode ? e.keyCode : e.which;
    lastCode = code;
    for (var i=0; i<codes.length; i++) {
        if (code == codes[i]) {
            send(chars[i]);
            return;
        }
    }
}

function keyup(e)
{
    var codes = [87, 65, 83, 68, 37, 38, 39, 40];
    var code;

    if (!keyPressed) {
        return;
    }
    keyPressed = false;

    e = e ? e : event;
    code = e.keyCode ? e.keyCode : e.which;
    for (var i=0; i<codes.length; i++) {
        if (code == codes[i]) {
            send('z');
            return;
        }
    }
}

function keypress(e)
{
    var chars = ['i', 'j', 'k', 'l', ];
    var codes = [105,  106,  107,  108, ];
    var code;

    e = e ? e : event;
    code = e.keyCode ? e.keyCode : e.which;

    for (var i=0; i<codes.length; i++) {
        if (code == codes[i]) {
            send(chars[i]);
            return;
        }
    }
}

function send(s)
{
    var url = "car.control?action=" + s;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, true);
    xmlHttp.send();
}
