// ======================================================
// Live Clock
// ======================================================

function updateClock() {

    const now = new Date();

    document.getElementById("liveTime").textContent =
        now.toLocaleDateString() +
        " | " +
        now.toLocaleTimeString();
}

setInterval(updateClock, 1000);
updateClock();


// ======================================================
// Chart Labels
// ======================================================

const labels = [];

for (let i = 1; i <= 10; i++) {

    labels.push(i.toString());

}


// ======================================================
// Chart Data
// ======================================================

const cpuData = Array(10).fill(0);

const memoryData = Array(10).fill(0);

const diskData = Array(10).fill(0);

const networkData = Array(10).fill(0);


// ======================================================
// CPU Chart
// ======================================================

const cpuChart = new Chart(

document.getElementById("cpuChart"),

{

type: "line",

data: {

labels: labels,

datasets: [{

label: "CPU Usage %",

data: cpuData,

borderColor: "#00e676",

backgroundColor: "rgba(0,230,118,.15)",

fill: true,

tension: .4

}]

},

options: {

responsive: true,

animation: false,

plugins: {

legend: {

labels: {

color: "white"

}

}

},

scales: {

x: {

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

},

y: {

beginAtZero: true,

max: 100,

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

}

}

}

});


// ======================================================
// Memory Chart
// ======================================================

const memoryChart = new Chart(

document.getElementById("memoryChart"),

{

type: "line",

data: {

labels: labels,

datasets: [{

label: "Memory %",

data: memoryData,

borderColor: "#03a9f4",

backgroundColor: "rgba(3,169,244,.15)",

fill: true,

tension: .4

}]

},

options: {

responsive: true,

animation: false,

plugins: {

legend: {

labels: {

color: "white"

}

}

},

scales: {

x: {

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

},

y: {

beginAtZero: true,

max: 100,

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

}

}

}

});


// ======================================================
// Disk Chart
// ======================================================

const diskChart = new Chart(

document.getElementById("diskChart"),

{

type: "bar",

data: {

labels: ["Root"],

datasets: [{

label: "Disk Usage %",

data: diskData,

backgroundColor: "#ff9800"

}]

},

options: {

responsive: true,

animation: false,

plugins: {

legend: {

labels: {

color: "white"

}

}

},

scales: {

x: {

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

},

y: {

beginAtZero: true,

max: 100,

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

}

}

}

});


// ======================================================
// Network Chart
// ======================================================

const networkChart = new Chart(

document.getElementById("networkChart"),

{

type: "line",

data: {

labels: labels,

datasets: [{

label: "Network",

data: networkData,

borderColor: "#ffc107",

backgroundColor: "rgba(255,193,7,.2)",

fill: true,

tension: .4

}]

},

options: {

responsive: true,

animation: false,

plugins: {

legend: {

labels: {

color: "white"

}

}

},

scales: {

x: {

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

},

y: {

ticks: {

color: "white"

},

grid: {

color: "#30363d"

}

}

}

}

});


// ======================================================
// Fetch Metrics
// ======================================================

async function fetchMetrics() {

    try {

        const response = await fetch("/metrics");

        const data = await response.json();

        document.getElementById("cpuValue").textContent =
            data.cpu.toFixed(2) + "%";

        document.getElementById("memoryValue").textContent =
            data.memory.toFixed(2) + "%";

        document.getElementById("diskValue").textContent =
            data.disk.toFixed(2) + "%";

        document.getElementById("cpuAvg").textContent =
            data.cpu.toFixed(2) + "%";

        document.getElementById("memoryAvg").textContent =
            data.memory.toFixed(2) + "%";

        document.getElementById("diskAvg").textContent =
            data.disk.toFixed(2) + "%";

        document.getElementById("cpuOverview").textContent =
            data.cpu.toFixed(2) + "%";

        document.getElementById("memoryOverview").textContent =
            data.memory.toFixed(2) + "%";

        document.getElementById("prometheusStatus").textContent =
            data.prometheus;

        document.getElementById("alertmanagerStatus").textContent =
            data.alertmanager;

        document.getElementById("activeAlerts").textContent =
            data.active_alerts;

        document.getElementById("lastUpdated").textContent =
            data.timestamp;

                    // ======================================================
        // Update Charts
        // ======================================================

        cpuData.push(data.cpu);
        cpuData.shift();
        cpuChart.update();

        memoryData.push(data.memory);
        memoryData.shift();
        memoryChart.update();

        diskData.push(data.disk);
        diskData.shift();
        diskChart.update();

        // Network graph (placeholder until network API available)

        networkData.push(0);
        networkData.shift();
        networkChart.update();

        // ======================================================
        // Footer Status
        // ======================================================

        document.getElementById("footerStatus").textContent = "ONLINE";

        document.getElementById("systemHealth").textContent =
            data.prometheus === "UP" &&
            data.alertmanager === "UP"
                ? "Healthy"
                : "Degraded";

        // ======================================================
        // Alerts Table
        // ======================================================

        const alertsTable =
            document.getElementById("alertsTable");

        alertsTable.innerHTML = "";

        if (data.alerts.length === 0) {

            alertsTable.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center">
                        No Active Alerts
                    </td>
                </tr>
            `;

        } else {

            data.alerts.forEach(alert => {

                alertsTable.innerHTML += `

                <tr>

                    <td>${alert.name}</td>

                    <td>${alert.severity}</td>

                    <td>${alert.state}</td>

                </tr>

                `;

            });

        }

    }

    catch (error) {

        console.error(error);

    }// ======================================================
// Fetch Recovery History
// ======================================================

async function fetchHistory() {

    try {

        const response = await fetch("/history");

        const history = await response.json();

        const historyTable =
            document.getElementById("historyTable");

        historyTable.innerHTML = "";

        if (history.length === 0) {

            historyTable.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center">
                        No Recovery History
                    </td>
                </tr>
            `;

            return;

        }

        history.reverse().forEach(item => {

            historyTable.innerHTML += `

            <tr>

                <td>${item.timestamp}</td>

                <td>${item.alert}</td>

                <td>${item.action}</td>

            </tr>

            `;

        });

    }

    catch (error) {

        console.error("History Error :", error);

    }

}


// ======================================================
// Dashboard Refresh
// ======================================================

async function refreshDashboard() {

    await fetchMetrics();

    await fetchHistory();

}


// ======================================================
// Initial Load
// ======================================================

refreshDashboard();


// ======================================================
// Auto Refresh Every 5 Seconds
// ======================================================

setInterval(() => {

    refreshDashboard();

}, 5000);


// ======================================================
// Connection Monitor
// ======================================================

window.addEventListener("online", () => {

    document.getElementById("footerStatus").textContent = "ONLINE";

});

window.addEventListener("offline", () => {

    document.getElementById("footerStatus").textContent = "OFFLINE";

});


// ======================================================
// Console Banner
// ======================================================

console.log(`
==========================================
 Self-Healing Infrastructure Dashboard
==========================================
 Prometheus  : Connected
 Alertmanager: Connected
 Auto Refresh: 5 Seconds
 Charts       : Live
 Recovery     : Enabled
==========================================
`);

}


