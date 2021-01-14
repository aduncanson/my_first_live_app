var call_outcome_chart = document.getElementById('call-outcome-chart').getContext('2d');
var services_chart = document.getElementById('services-chart').getContext('2d');
var brands_chart = document.getElementById('brands-chart').getContext('2d');
var myPieCallOutcome = "";
var myPieServices = "";
var myPieBrands = "";
window.onload = function() {
    myPieCallOutcome = new Chart(call_outcome_chart, call_outcome_chart_config);
    myPieServices = new Chart(services_chart, services_chart_config);
    myPieBrands = new Chart(brands_chart, brands_chart_config);
};
function toggleBorder(o){
    o.classList.toggle("selectedBorder");
}
function chnage_graph_type(o, graph){
    o.classList.toggle("make-pie-chart");
    o.classList.toggle("make-bar-chart");
    if (graph == 'call-outcome') {
        myPieCallOutcome.destroy();
        if (call_outcome_chart_config.type == "pie") {
            call_outcome_chart_config.type = "bar";
            call_outcome_chart_config.options.scales.xAxes[0].display = true;
            call_outcome_chart_config.options.scales.yAxes[0].display = true;
        } else {
            call_outcome_chart_config.type = "pie";
            call_outcome_chart_config.options.scales.xAxes[0].display = false;
            call_outcome_chart_config.options.scales.yAxes[0].display = false;
        }
        myPieCallOutcome = new Chart(call_outcome_chart, call_outcome_chart_config);
    } else if (graph == 'services') {
        myPieServices.destroy();
        if (services_chart_config.type == "pie") {
            services_chart_config.type = "bar";
            services_chart_config.options.scales.xAxes[0].display = true;
            services_chart_config.options.scales.yAxes[0].display = true;
        } else {
            services_chart_config.type = "pie";
            services_chart_config.options.scales.xAxes[0].display = false;
            services_chart_config.options.scales.yAxes[0].display = false;
        }
        myPieServices = new Chart(services_chart, services_chart_config);
    } else if (graph == 'brands') {
        myPieBrands.destroy();
        if (brands_chart_config.type == "pie") {
            brands_chart_config.type = "bar";
            brands_chart_config.options.scales.xAxes[0].display = true;
            brands_chart_config.options.scales.yAxes[0].display = true;
        } else {
            brands_chart_config.type = "pie";
            brands_chart_config.options.scales.xAxes[0].display = false;
            brands_chart_config.options.scales.yAxes[0].display = false;
        }
        myPieBrands = new Chart(brands_chart, brands_chart_config);
    }
}