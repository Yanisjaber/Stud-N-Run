(function(){
  var el=document.getElementById('map3d'); if(!el||!window.maplibregl) return;
  fetch('assets/parcours.geojson').then(function(r){return r.json()}).then(function(f){
    var line=f.geometry.coordinates, start=line[0];
    var map=new maplibregl.Map({container:el,style:'https://tiles.openfreemap.org/styles/liberty',center:start,zoom:15.2,pitch:62,bearing:-20,maxPitch:80,attributionControl:{compact:true}});
    map.addControl(new maplibregl.NavigationControl({visualizePitch:true}),'top-right');
    // distances cumulées (m)
    function dist(a,b){var R=6371000,x=(b[0]-a[0])*Math.PI/180*Math.cos(a[1]*Math.PI/180),y=(b[1]-a[1])*Math.PI/180;return R*Math.sqrt(x*x+y*y)}
    var cum=[0];for(var i=1;i<line.length;i++)cum.push(cum[i-1]+dist(line[i-1],line[i]));
    var total=cum[cum.length-1];
    function at(s){s=Math.max(0,Math.min(total,s));var i=1;while(i<cum.length-1&&cum[i]<s)i++;var t=(s-cum[i-1])/Math.max(cum[i]-cum[i-1],1e-9);return [line[i-1][0]+(line[i][0]-line[i-1][0])*t,line[i-1][1]+(line[i][1]-line[i-1][1])*t]}
    function bearing(a,b){var y=Math.sin((b[0]-a[0])*Math.PI/180)*Math.cos(b[1]*Math.PI/180),x=Math.cos(a[1]*Math.PI/180)*Math.sin(b[1]*Math.PI/180)-Math.sin(a[1]*Math.PI/180)*Math.cos(b[1]*Math.PI/180)*Math.cos((b[0]-a[0])*Math.PI/180);return (Math.atan2(y,x)*180/Math.PI+360)%360}
    map.on('load',function(){
      map.addSource('route',{type:'geojson',data:f});
      map.addLayer({id:'route-halo',type:'line',source:'route',layout:{'line-join':'round','line-cap':'round'},paint:{'line-color':'#fff','line-width':11}});
      map.addLayer({id:'route-line',type:'line',source:'route',layout:{'line-join':'round','line-cap':'round'},paint:{'line-color':'#a2145d','line-width':6}});
      for(var k=1;k<=4;k++){var d=document.createElement('div');d.className='km-marker';d.textContent=k+' km';new maplibregl.Marker({element:d}).setLngLat(at(k*1000)).addTo(map)}
      var s=document.createElement('div');s.className='start-marker';s.textContent='Départ / arrivée';
      new maplibregl.Marker({element:s,anchor:'bottom'}).setLngLat(start).addTo(map);
    });
    var anim=null,btn=document.getElementById('fly-btn');
    function stop(){if(anim){cancelAnimationFrame(anim);anim=null}btn.textContent='▶ Survoler le parcours'}
    btn.addEventListener('click',function(){
      if(anim){stop();return}
      btn.textContent='■ Arrêter';var t0=null,dur=60000,lastB=null;
      function step(ts){
        if(t0===null)t0=ts;var p=(ts-t0)/dur;if(p>=1){stop();return}
        var s=p*total,c=at(s),n=at(s+120),b=bearing(c,n);
        lastB=lastB===null?b:lastB+((((b-lastB)%360)+540)%360-180)*0.06;
        map.jumpTo({center:c,bearing:lastB,pitch:68,zoom:16.3});
        anim=requestAnimationFrame(step)}
      anim=requestAnimationFrame(step)});
    ['mousedown','wheel','touchstart'].forEach(function(e){el.addEventListener(e,function(){if(anim)stop()},{passive:true})});
    document.getElementById('reset-btn').addEventListener('click',function(){stop();map.flyTo({center:start,zoom:15.2,pitch:62,bearing:-20})});
  });
})();
