/*
 * Javascript file to implement client side usability for
 * Operating Systems Desing exercises.
 */
var server_address = "http://35.198.162.23:5000/";
var filter_device = "";
var filter_latitude = 0;
var filter_longitude = 0;
var filter_state = "";
var table_measures = null;
var table_devices = null;
var device_interval = null;
var measures_interval = null;
var update_time_ms = 3000;

var last_map_lat_lon = []

var get_current_sensor_data = function() {
    device_details = "<h2>Dispositivo: "+filter_device+" - "+filter_state+" - "+deg_to_string(filter_latitude)+";"+deg_to_string(filter_longitude)+"</h2>"
    $("#device_details").html(device_details);
	$.getJSON( server_address+"dso/measurements/", function( data_list ) {
        table_measures.clear();
        for (let i = 0; i < data_list.length; i++) {
                if (data_list[i].temperature != 0 && data_list[i].humidity != 0){
                    table_measures.row.add( 
                        [
                        data_list[i].time,
                        data_list[i].temperature,
                        data_list[i].humidity,
                        data_list[i].device_id,
                        ]);
                }
        }
        table_measures.draw();
	});
}

var get_device_list = function() {
	$.getJSON( server_address+"dso/devices/", function( data_list ) {
        table_devices.clear();
        for (let i = 0; i < data_list.length; i++) {
            table_devices.row.add( [
                data_list[i].device_id,
                data_list[i].state,
                deg_to_string(data_list[i].latitude),
                deg_to_string(data_list[i].longitude),
                data_list[i].time,
                "<div class=\"button_container\"><button class=\"device_btn\" id=\""+data_list[i].device_id+"\">Medidas</button></div>"
            ]).draw();
            
            if (data_list.length > last_map_lat_lon.length ||
                 deg_to_decimal(data_list[i].latitude) != last_map_lat_lon[i][0] ||
                 deg_to_decimal(data_list[i].longitude) != last_map_lat_lon[i][1]) {
                last_map_lat_lon.push([deg_to_decimal(data_list[i].latitude), deg_to_decimal(data_list[i].longitude)]);
                $("#myMap").am_map( 'addLayer', {zoom: 5, 'name' : data_list[i].device_id, 'points' : [deg_to_decimal(data_list[i].latitude), deg_to_decimal(data_list[i].longitude),{'name':data_list[i].device_id, 'desc':data_list[i].state}] });
            }
        }
        table_devices.draw();
        $(".device_btn").click(function(){
            last_map_lat_lon = []
            filter_device = this.id;
            for (let i = 0; i < data_list.length; i++) {
                if(data_list[i].device_id == filter_device){
                    filter_latitude = deg_to_decimal(data_list[i].latitude);
                    filter_longitude = deg_to_decimal(data_list[i].longitude);
                    filter_state = data_list[i].state;
                }
            }
            

            devices_hide();
            measures_show();

            $('#min, #max').change( function() {
                table_measures.draw();
            } );
            get_current_sensor_data();
            measures_interval = setInterval(get_current_sensor_data,update_time_ms,);
            clearInterval(device_interval);
            $("#volver").click(function(){
                
                last_map_lat_lon = []
                measures_hide();
                devices_show();
                get_device_list();
                device_interval = setInterval(get_device_list,update_time_ms);
                clearInterval(measures_interval);
            });
        });
	});
}

/* Custom filtering function which will search data in column four between two values */
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = Date.parse( $('#min').val());
        var max = Date.parse( $('#max').val());
        var fecha = Date.parse( data[0] ) || 0;
        var device_id = data[3] || 0;
 
        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && fecha <= max ) ||
             ( min <= fecha   && isNaN( max ) ) ||
             ( min <= fecha   && fecha <= max ) )
        {
            if (device_id == filter_device){
                return true;
            }
        }
        return false;
    }
);
         
$.fn.dataTable.ext.type.order['fecha-pre'] = function ( d ) {
    return d.split(", ")[1];
};

$(document).ready(function() {
    measures_hide();
    devices_show();
    table_devices = $('#device_table').DataTable(
        {"bFilter":false,
        "paging":false,
        "responsive": true
        }
    );
    table_measures = $('#measures_table').DataTable({
        "columnDefs": [ {
        "type": "fecha",
        "targets": 0
        },
        {
            "targets":-1,
            "visible":false
        }],
        "paging":false,
        "responsive": true
    });  
    get_device_list();
    device_interval = setInterval(get_device_list,update_time_ms);        
        
});

function measures_hide(){
    $(".measures").css("display", "none");
}

function measures_show(){
    $(".measures").css("display", "block");
}

function devices_hide(){
    $(".device").css("display", "none");
    $(".map_container").html(function(index,oldHTML){
        return "";
    });
}

function devices_show(){
    $(".device").css("display", "block");

    $(".map_container").html(function(index,oldHTML){
        return "<div id=\"myMap\"></div>";
    });
    $("#myMap").am_map({
        center: [filter_latitude, filter_longitude],
        height:'400px',
        background:'osm',
    });
}
/**
 * @param {float} number - The number
 */
function deg_to_decimal(number){
    
    let degree = parseInt(number % 100);
    let str = String(number - degree + 0.00001);
    let min = 0
    let sec = 0
    if (str[0] == '-') {
        min = -parseInt(str[3]+str[4]);
        sec = -parseInt(str[5]+str[6]);
        
    }else{
        min = parseInt(str[2]+str[3]);
        sec = parseInt(str[4]+str[5]);

    }
    return degree + min / 60 + sec / 3600;
}

function deg_to_string(number){
    
    let degree = parseInt(number % 100);
    let str = String(number - degree + 0.00001);
    let min = 0
    let sec = 0
    if (str[0] == '-') {
        min = parseInt(str[3]+str[4]);
        sec = parseInt(str[5]+str[6]);
    }else{
        min = parseInt(str[2]+str[3]);
        sec = parseInt(str[4]+str[5]);
    }
    
    return String(degree)+"&#176;"+String(min)+"'"+String(sec)+'"'
    
}
