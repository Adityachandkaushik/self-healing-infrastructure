// =============================
// Live Clock
// =============================

function updateClock() {

    const now = new Date();

    document.getElementById("liveTime").innerHTML =
        now.toLocaleDateString() +
        " | " +
        now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// =============================
// Random Generator
// =============================

function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


// =============================
// Common Chart Config
// =============================

const labels = [
    "1","2","3","4","5","6","7","8"
];


// =============================
// CPU Chart
// =============================

const cpuChart = new Chart(

document.getElementById("cpuChart"),

{

type:"line",

data:{

labels:labels,

datasets:[{

label:"CPU Usage %",

data:[35,42,38,60,55,48,63,50],

borderColor:"#00e676",

backgroundColor:"rgba(0,230,118,.15)",

fill:true,

tension:.4

}]

},

options:{

responsive:true,

plugins:{
legend:{
labels:{
color:"white"
}
}
},

scales:{

x:{
ticks:{color:"white"},
grid:{color:"#30363d"}
},

y:{
ticks:{color:"white"},
grid:{color:"#30363d"},
beginAtZero:true,
max:100
}

}

}

});


// =============================
// Memory Chart
// =============================

const memoryChart = new Chart(

document.getElementById("memoryChart"),

{

type:"line",

data:{

labels:labels,

datasets:[{

label:"Memory %",

data:[55,52,58,60,62,59,65,68],

borderColor:"#03a9f4",

backgroundColor:"rgba(3,169,244,.15)",

fill:true,

tension:.4

}]

},

options:{

responsive:true,

plugins:{
legend:{
labels:{color:"white"}
}
},

scales:{

x:{
ticks:{color:"white"},
grid:{color:"#30363d"}
},

y:{
ticks:{color:"white"},
grid:{color:"#30363d"},
beginAtZero:true,
max:100
}

}

}

});


// =============================
// Disk Chart
// =============================

const diskChart = new Chart(

document.getElementById("diskChart"),

{

type:"bar",

data:{

labels:["Root","Home","Docker","Logs"],

datasets:[{

label:"Disk Usage",

data:[60,72,45,33],

backgroundColor:[
"#00e676",
"#ff9800",
"#03a9f4",
"#f44336"
]

}]

},

options:{

plugins:{
legend:{
labels:{color:"white"}
}
},

scales:{

x:{
ticks:{color:"white"},
grid:{color:"#30363d"}
},

y:{
ticks:{color:"white"},
grid:{color:"#30363d"},
beginAtZero:true,
max:100
}

}

}

});


// =============================
// Network Chart
// =============================

const networkChart = new Chart(

document.getElementById("networkChart"),

{

type:"line",

data:{

labels:labels,

datasets:[{

label:"Network MB/s",

data:[12,18,15,20,16,24,19,25],

borderColor:"#ff9800",

backgroundColor:"rgba(255,152,0,.2)",

fill:true,

tension:.4

}]

},

options:{

plugins:{
legend:{
labels:{color:"white"}
}
},

scales:{

x:{
ticks:{color:"white"},
grid:{color:"#30363d"}
},

y:{
ticks:{color:"white"},
grid:{color:"#30363d"}
}

}

}

});



// =============================
// Auto Update Charts
// =============================

setInterval(()=>{

cpuChart.data.datasets[0].data.shift();
cpuChart.data.datasets[0].data.push(random(25,90));
cpuChart.update();

memoryChart.data.datasets[0].data.shift();
memoryChart.data.datasets[0].data.push(random(40,90));
memoryChart.update();

networkChart.data.datasets[0].data.shift();
networkChart.data.datasets[0].data.push(random(10,35));
networkChart.update();

diskChart.data.datasets[0].data=[
random(30,80),
random(30,80),
random(30,80),
random(30,80)
];

diskChart.update();

},3000);



// =============================
// Auto Refresh Page Data
// =============================

setInterval(()=>{

console.log("Dashboard Refreshed");

},5000);