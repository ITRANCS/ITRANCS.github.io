var isPlay = true
				var steps = 0
				var counter = 0
				var newRouteGeoJson = {}
		        var point = {
								'type': 'FeatureCollection',
								'features': [
								{
								'type': 'Feature',
								'properties': {},
								'geometry': {
								'type': 'Point',
								'coordinates': []
								}
								}
								]
							};
				function animate() {
					var start =
					newRouteGeoJson.features[0].geometry.coordinates[
					counter >= steps ? counter - 1 : counter
					];
					var end =
					newRouteGeoJson.features[0].geometry.coordinates[
					counter >= steps ? counter : counter + 1
					];
					if (!start || !end) return;
					 
					// Update point geometry to a new position based on counter denoting
					// the index to access the arc
					point.features[0].geometry.coordinates =
					newRouteGeoJson.features[0].geometry.coordinates[counter];
					 
					// Calculate the bearing to ensure the icon is rotated to match the route arc
					// The bearing is calculated between the current point and the next point, except
					// at the end of the arc, which uses the previous point and the current point
					point.features[0].properties.bearing = turf.bearing(
					turf.point(start),
					turf.point(end)
					);
					 
					// Update the source with this new data
					map.getSource('point').setData(point);
					 
					// Request the next frame of animation as long as the end has not been reached
					if (counter < steps) {
					requestAnimationFrame(animate);
					}
					 
					counter = counter + 1;
				}

		        function lineMore(from, to, distance, splitLength, units) {
		            var step = parseInt(distance / splitLength)
		            var leftLength = distance - step * splitLength
		            var rings = []
		            var route = turf.linestring([from.geometry.coordinates, to.geometry.coordinates])
		            for (let i = 1; i <= step; i++) {
		                let nlength = i * splitLength
		                let pnt = turf.along(route, nlength, units);
		                rings.push(pnt.geometry.coordinates)
		            }
		            if (leftLength > 0) {
		                rings.push(to.geometry.coordinates)
		            }
		            return rings
		        }

		        function resetRoute(route, nstep, units) {
		            var newroute = {
		                'type': 'FeatureCollection',
				        'features': [
				            {
				                'type': 'Feature',
				                'geometry': {
				                'type': 'LineString',
				                'coordinates': []
				                }
				            }
				        ]
		            }
		            var lineDistance = turf.lineDistance(route);
		            var nDistance = lineDistance / nstep;
		            var aLength = route.geometry.coordinates.length;
		            for (let i = 0; i < aLength - 1; i++) {
		                var from = turf.point(route.geometry.coordinates[i]);
		                var to = turf.point(route.geometry.coordinates[i + 1]);
		                let lDistance = turf.distance(from, to, units);
		                if (i == 0) {
		                    newroute.features[0].geometry.coordinates.push(route.geometry.coordinates[0])
		                }
		                if (lDistance > nDistance) {
		                    let rings = lineMore(from, to, lDistance, nDistance, units)
		                    newroute.features[0].geometry.coordinates = newroute.features[0].geometry.coordinates.concat(rings)
		                } else {
		                    newroute.features[0].geometry.coordinates.push(route.geometry.coordinates[i + 1])
		                }
		            }
		            return newroute
		        }
		        function play(){
		        	// Reset the counter
					counter = 0;
							 
					// Restart the animation
					animate(counter);
		        }
				function route(){
					document.getElementById("routeDialog").close();
					var src=document.getElementById('src');
					var des=document.getElementById('des');
					$.ajax({
	                url: 'http://127.0.0.1:5001/route',
	                data:{
	                  src: src.value,
	                  des: des.value
	                },
	                dataType: 'JSON',
	                type: 'GET',
	                success: function(data){
	                	if(data['status'] == 'success')
	                	{
	                		
	                		var routeGeoJson = data['geojson']
							
				            // A single point that animates along the route.
							// Coordinates are initially set to origin.
							map.addLayer({
				                'id': 'routeLayer',
				                'type': 'line',
				                'source': {
				                    'type': 'geojson',
				                    'lineMetrics': true,
				                    'data': data['geojson']
				                },
				                'paint': {
				                    'line-width': 7,
				                    'line-opacity': 1,
				                    'line-color': '#009EFF',
				                }
				            });
							map.addLayer({
				                'id': 'arrowLayer',
				                'type': 'symbol',
				                'source': {
				                    'type': 'geojson',
				                    'data': data['geojson'] //轨迹geojson格式数据
				                },
				                'layout': {
				                    'symbol-placement': 'line',
				                    'symbol-spacing': 50, // 图标间隔，默认为250
				                    'icon-image': 'arrowIcon', //箭头图标
				                    'icon-size': 0.5
				                }
				            });

						
							map.addSource('point', {
							'type': 'geojson',
							'data': point
							});
							 
							map.addLayer({
							'id': 'point',
							'source': 'point',
							'type': 'symbol',
							'layout': {
							'icon-image': 'pulsing-dot'
							}
							});
				            
				            
							newRouteGeoJson = resetRoute(data['geojson'].features[0], 1000, 'kilometers')

							map.getSource('routeLayer').setData(newRouteGeoJson);
							map.getSource('arrowLayer').setData(newRouteGeoJson);
							


							point.features[0].geometry.coordinates = data['geojson'].features[0].geometry.coordinates[0];
							steps = newRouteGeoJson.features[0].geometry.coordinates.length
							 
							// Update the source layer
							map.getSource('point').setData(point);          

				            if('aslist' in data)
				            {
				            	for(var k in data['aslist'])
				            	{
				            		var coor = data['geojson'].features[0].geometry.coordinates
				            		var lat = coor[k][1]
			                		var lng = coor[k][0]
			                		var popup = new mapboxgl.Popup({ offset: 25 }).setText(
									data['aslist'][k]
									);
									var marker = new mapboxgl.Marker()
									  .setLngLat([lng, lat])
									  .setPopup(popup)
									  .addTo(map);
				            	}
				            }
				            

				            if('iplist' in data)
				            {
				            	for(var k in data['iplist'])
				            	{
				            		var coor = data['geojson'].features[0].geometry.coordinates
				            		var lat = coor[k][1]
			                		var lng = coor[k][0]
			                		var popup = new mapboxgl.Popup({ offset: 25 }).setText(
									data['iplist'][k]
									);
									var marker = new mapboxgl.Marker()
									  .setLngLat([lng, lat])
									  .setPopup(popup)
									  .addTo(map);
				            	}
				            }

				            var bs = document.getElementById("zoom");
          					bs.style.display="block";


	      //           		var lat = data['lat']
	      //           		var lng = data['lng']
	      //           		var popup = new mapboxgl.Popup({ offset: 25 }).setText(
							// name.value
							// );
							// var marker = new mapboxgl.Marker()
							//   .setLngLat([lng, lat])
							//   .setPopup(popup)
							//   .addTo(map);
							// map.flyTo({center:[lng, lat],zoom:11})
							// map.setZoom(11)
	                	}
	                	else if(data['status'] == 'failed')
	                	{
	                		alert('failed!')
	                	}
	                	
	                }
	                });
				}