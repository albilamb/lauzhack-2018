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
            $(".list-group").append('<div id='+ i +' class="list-group-item justify-content-between" style="cursor: pointer"><a href="#modal-container-447899" role="button" data-toggle="modal">'+ data[i].name +'</a></div>');
            if (data[i].exotic) {
                $("#"+i).append('<span class="badge badge-pill badge-primary">Exotic</span>');
            }
            $("#"+i).click(function(e){
                var q = e.target.innerText;
                $.getJSON("http://127.0.0.1:5000/placedetails?place1=" + p1 + "&place2=" + p2 + "&place3=" + p3 + "&query=" + q, function(data){
                    console.log(data)
                })
            })
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
        var fastest = data.split(',')[0];
        window.localStorage.setItem("fastest", fastest);
        $.getJSON("http://127.0.0.1:5000/recommended?place1="+ p1 + "&place2=" + p2 + "&place3=" + p3, function(data){
            console.log(data)
            var r1 = "Take a " + data[0].place1.Name + " which takes " + data[0].place1.Duration + " mins and costs around " + data[0].place1.Price + " USD approx";
            var r2 = "Take a " + data[0].place2.Name + " which takes " + data[0].place2.Duration + " mins and costs around " + data[0].place2.Price + " USD approx";
            var r3 = "Take a " + data[0].place3.Name + " which takes " + data[0].place3.Duration + " mins and costs around " + data[0].place3.Price + " USD approx";
            $("#routes").append('<h5 class="card-header">'+ p1 + ' -> ' + fastest +'</h5><p>'+r1+'</p>');
            $("#routes").append('<h5 class="card-header">'+ p2 + ' -> ' + fastest +'</h5><p>'+r2+'</p>');
            $("#routes").append('<h5 class="card-header">'+ p3 + ' -> ' + fastest +'</h5><p>'+r3+'</p>');
        });
    });
    $.getJSON("http://127.0.0.1:5000/cheapestplace?place1=" + p1 + "&place2=" + p2 + "&place3=" + p3, function(data){
        var k = window.localStorage.getItem(data.split(',')[0]);
        console.log(k);
        $("#"+k).append('<span class="badge badge-pill badge-primary">Cheapest</span>')
        window.localStorage.setItem("cheapest", data.split(',')[0]);
    });
});