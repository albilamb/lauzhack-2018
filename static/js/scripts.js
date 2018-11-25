var lastXhr;
var latLngMap = {};
$( "#demo1" ).autocomplete({
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
        console.log(marker)
    }
});

$( "#demo2" ).autocomplete({
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