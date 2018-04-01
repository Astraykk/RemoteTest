var List = {{ List|safe }};
var Dict = {{ Dict|safe }};

document.getElementById("demo").innerHTML={{ List|safe }}
//document.getElementById("demo").innerHTML= Dict

    var cntx=mycanvas.getContext('2d');
    cntx.lineCap = 'round';
    cntx.strokeStyle = '#ffff00';
    cntx.lineWidth = 4;
    function turn_it(){
        cntx.beginPath();
        cntx.moveTo(0, 0);
        move_num = 0.1;
        rads = rotate_num * 2 * Math.PT;
        for (i=1;i<=100;i++){
            distance = i * move_num;
            turn = i * rads;
            x = Math.cos(turn) * distance;
            y = Math.sin(turn) * distance;
            cntx.lineTo(x, y);
        }
    }
    cntx.translate(cntx.canvas.width/2, cntx.canvas.height/2);
    setInterval(
        function(){
            cntx.clearRect(-cntx.canvas.width/2, -cntx.canvas.height/2, cntx.canvas.width, cntx.canvas.height);
            cntx.rotate(.01);
            turn_it.apply();
            cntx.stroke();
        }, 10);

