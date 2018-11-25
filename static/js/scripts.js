var lastXhr;
var latLngMap = {};
var icons = ['http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png','http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'];
var iconIndex=0;

$('a[href*=\\#]').on('click', function(e) {
    e.preventDefault();
    console.log($(this))
    $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top}, 500, 'linear');
  });

window.localStorage.clear();
$( "#demo1" ).autocomplete({
    appendTo: "#form1",
    source: function( request, response ) {
        if (lastXhr) lastXhr.abort();
        lastXhr = $.getJSON( "http://127.0.0.1:5000/geocode?query=" + request.term, request, function( data, status, xhr ) {
            if ( xhr === lastXhr ) {
                
                var tmp = [];
                for (var i in data.places) {
                    tmp.push(data.places[i].longName);
                    latLngMap[data.places[i].longName] = {lat: data.places[i].lat, lng: data.places[i].lng};
                }
                response( tmp );
            }
        });
    },
    select: function( event, item ) {
        var mark = latLngMap[item.item.label];
        // $.getJSON("http://127.0.0.1:5000/update-marker?lat=" + mark.lat + "&lng=" + mark.lng, function(data){
        //     console.log(data);
        // });
        // console.log(jsmap)
        console.log(window.map)
        var marker = new google.maps.Marker({position: mark, label: "Shiva", map: window.map})
        $(".ui-helper-hidden-accessible").css("display", "none");
        console.log(marker)
    }
});

$( "#demo2" ).autocomplete({
    appendTo: "#form2",
    source: function( request, response ) {
        if (lastXhr) lastXhr.abort();
        lastXhr = $.getJSON( "http://127.0.0.1:5000/geocode?query=" + request.term, request, function( data, status, xhr ) {
            if ( xhr === lastXhr ) {
                
                var tmp = [];
                for (var i in data.places) {
                    tmp.push(data.places[i].longName);
                    latLngMap[data.places[i].longName] = {lat: data.places[i].lat, lng: data.places[i].lng};
                }
                response( tmp );
            }
        });
    },
    select: function( event, item ) {
        var mark = latLngMap[item.item.label];
        console.log(item.item.label)
        console.log()
        // $.getJSON("http://127.0.0.1:5000/update-marker?lat=" + mark.lat + "&lng=" + mark.lng, function(data){
        //     console.log(data);
        // });
        // console.log(jsmap)
        console.log(mark)
        var marker = new google.maps.Marker({position: mark, label: "Kajal", map: window.map})
        console.log(marker)
    }
});

$( "#demo3" ).autocomplete({
    appendTo: "#form3",
    source: function( request, response ) {
        if (lastXhr) lastXhr.abort();
        lastXhr = $.getJSON( "http://127.0.0.1:5000/geocode?query=" + request.term, request, function( data, status, xhr ) {
            if ( xhr === lastXhr ) {
                
                var tmp = [];
                for (var i in data.places) {
                    tmp.push(data.places[i].longName);
                    latLngMap[data.places[i].longName] = {lat: data.places[i].lat, lng: data.places[i].lng};
                }
                response( tmp );
            }
        });
    },
    select: function( event, item ) {
        var mark = latLngMap[item.item.label];
        // $.getJSON("http://127.0.0.1:5000/update-marker?lat=" + mark.lat + "&lng=" + mark.lng, function(data){
        //     console.log(data);
        // });
        // console.log(jsmap)
        console.log(mark)
        var marker = new google.maps.Marker({position: mark, label: "Sricharan", map: window.map})
        console.log(marker)
    }
});

$("#search").click(function(){
    var p1 = $("#demo1")[0].value;
    var p2 = $("#demo2")[0].value;
    var p3 = $("#demo3")[0].value;

    $.getJSON("http://127.0.0.1:5000/allplaces?place1=" + p1 + "&place2=" + p2 + "&place3=" + p3, function(data){
        for (var i=0; i<data.length; i++) {
            $(".list-group").append('<div id='+ i +' class="list-group-item justify-content-between" style="cursor: pointer">'+ data[i].name +'</div>');
            var marker = new google.maps.Marker({position: {lat: data[i].lat, lng: data[i].lng}, label: data[i].name, map: window.map, icon: icons[iconIndex++ % icons.length]});
            window.localStorage.setItem(data[i].name, i);
        }
        window.localStorage.setItem("cities", JSON.stringify(data));
        $(".list-group").jAnimateSequence(['tada']);
    });
    $.getJSON("http://127.0.0.1:5000/fastestplace?place1=" + p1 + "&place2=" + p2 + "&place3=" + p3, function(data){
        var k = window.localStorage.getItem(data.split(',')[0]);
        console.log(k);
        $("#"+k).append('<span class="badge badge-pill badge-primary">Fastest</span>')
    });
    $.getJSON("http://127.0.0.1:5000/cheapestplace?place1=" + p1 + "&place2=" + p2 + "&place3=" + p3, function(data){
        var k = window.localStorage.getItem(data.split(',')[0]);
        console.log(k);
        $("#"+k).append('<span class="badge badge-pill badge-primary">Cheapest</span>')
    });
});