mapboxgl.accessToken = 'pk.eyJ1IjoiZGljZXd1IiwiYSI6ImNrbGYzNjQzdzNsMXgybnBlZmxyZ3ljbDYifQ.4EWD0PYu_Yy5oZsWT0ZLjA';
			    var map = new mapboxgl.Map({
			        container: 'map',
			        style: 'mapbox://styles/mapbox/streets-v11',
			        zoom: 1.2,
			        center: [160, 20],
			        doubleClickZoom: false
			    });
			    mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.2.3/mapbox-gl-rtl-text.js');
				map.addControl(new MapboxLanguage({
				  defaultLanguage: 'zh-Hans'
				}));
				// map.addControl(new mapboxgl.FullscreenControl(),'top-left');

				/* given a query in the form "lng, lat" or "lat, lng" returns the matching
				* geographic coordinate(s) as search results in carmen geojson format,
				* https://github.com/mapbox/carmen/blob/master/carmen-geojson.md
				*/
				var coordinatesGeocoder = function (query) {
				// match anything which looks like a decimal degrees coordinate pair
				var matches = query.match(
				/^[ ]*(?:Lat: )?(-?\d+\.?\d*)[, ]+(?:Lng: )?(-?\d+\.?\d*)[ ]*$/i
				);
				if (!matches) {
				return null;
				}
				 
				function coordinateFeature(lng, lat) {
				return {
				center: [lng, lat],
				geometry: {
				type: 'Point',
				coordinates: [lng, lat]
				},
				place_name: 'Lat: ' + lat + ' Lng: ' + lng,
				place_type: ['coordinate'],
				properties: {},
				type: 'Feature'
				};
				}
				 
				var coord1 = Number(matches[1]);
				var coord2 = Number(matches[2]);
				var geocodes = [];
				 
				if (coord1 < -90 || coord1 > 90) {
				// must be lng, lat
				geocodes.push(coordinateFeature(coord1, coord2));
				}
				 
				if (coord2 < -90 || coord2 > 90) {
				// must be lat, lng
				geocodes.push(coordinateFeature(coord2, coord1));
				}
				 
				if (geocodes.length === 0) {
				// else could be either lng, lat or lat, lng
				geocodes.push(coordinateFeature(coord1, coord2));
				geocodes.push(coordinateFeature(coord2, coord1));
				}
				 
				return geocodes;
				};
				 
				// map.addControl(
				// new MapboxGeocoder({
				// accessToken: mapboxgl.accessToken,
				// localGeocoder: coordinatesGeocoder,
				// zoom: 4,
				// placeholder: '请输入经纬度查询位置',
				// mapboxgl: mapboxgl
				// })
				// );

				// 箭头-右
		        var svgXML =
		            `<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"> 
		                <path d="M529.6128 512L239.9232 222.4128 384.7168 77.5168 819.2 512 384.7168 946.4832 239.9232 801.5872z" p-id="9085" fill="#ffffff"></path> 
		            </svg>
		            `
		        // 箭头-上
		        // var svgXML =
		        // `<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"> 
		        //     <path d="M957.3 543.4L870.7 630 512.1 271.5 152.3 631.3l-86.6-86.6L512.1 98.2z" p-id="9085" fill="#ffffff"></path> 
		        // </svg>
		        // `
		        //给图片对象写入base64编码的svg流
		        var svgBase64 = 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(svgXML)));

		        var size = 100;

		        // implementation of CustomLayerInterface to draw a pulsing dot icon on the map
				// see https://docs.mapbox.com/mapbox-gl-js/api/#customlayerinterface for more info
				var pulsingDot = {
				width: size,
				height: size,
				data: new Uint8Array(size * size * 4),
				 
				// get rendering context for the map canvas when layer is added to the map
				onAdd: function () {
				var canvas = document.createElement('canvas');
				canvas.width = this.width;
				canvas.height = this.height;
				this.context = canvas.getContext('2d');
				},
				 
				// called once before every frame where the icon will be used
				render: function () {
				var duration = 1000;
				var t = (performance.now() % duration) / duration;
				 
				var radius = (size / 2) * 0.3;
				var outerRadius = (size / 2) * 0.7 * t + radius;
				var context = this.context;
				 
				// draw outer circle
				context.clearRect(0, 0, this.width, this.height);
				context.beginPath();
				context.arc(
				this.width / 2,
				this.height / 2,
				outerRadius,
				0,
				Math.PI * 2
				);
				context.fillStyle = 'rgba(255, 200, 200,' + (1 - t) + ')';
				context.fill();
				 
				// draw inner circle
				context.beginPath();
				context.arc(
				this.width / 2,
				this.height / 2,
				radius,
				0,
				Math.PI * 2
				);
				context.fillStyle = 'rgba(255, 100, 100, 1)';
				context.strokeStyle = 'white';
				context.lineWidth = 2 + 4 * (1 - t);
				context.fill();
				context.stroke();
				 
				// update this image's data with data from the canvas
				this.data = context.getImageData(
				0,
				0,
				this.width,
				this.height
				).data;
				 
				// continuously repaint the map, resulting in the smooth animation of the dot
				map.triggerRepaint();
				 
				// return `true` to let the map know that the image was updated
				return true;
				}
				};

		        map.on('load', function() {
		            let arrowIcon = new Image(20, 20)
		            arrowIcon.src = svgBase64
		            arrowIcon.onload = function() {
		                map.addImage('arrowIcon', arrowIcon);
		                map.addImage('pulsing-dot', pulsingDot, { pixelRatio: 2 });
		            }
		        });