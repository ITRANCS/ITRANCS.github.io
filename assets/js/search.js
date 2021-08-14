function searchb(){
					document.getElementById("searchbarDialog").showModal(); 
				}
				function routeb(){
					document.getElementById("routeDialog").showModal();
				}
				function search(){
					document.getElementById("searchbarDialog").close();
					var name=document.getElementById('text');
					$.ajax({
	                url: 'http://127.0.0.1:5000/search',
	                data:{
	                  name: name.value
	                },
	                dataType: 'JSON',
	                type: 'GET',
	                success: function(data){
	                	if(data['type'] == 'ip2geo')
	                	{
	                		var lat = data['lat']
	                		var lng = data['lng']
	                		var popup = new mapboxgl.Popup({ offset: 25 }).setText(
							name.value
							);
							var marker = new mapboxgl.Marker()
							  .setLngLat([lng, lat])
							  .setPopup(popup)
							  .addTo(map);
							map.flyTo({center:[lng, lat],zoom:11})
							// map.setZoom(11)
	                	}
	                	else if(data['type'] == 'as2geo')
	                	{
	                		var colors=new Array("#83AF9B","#FE4365","#F4D000","#65934A","#1E293D","#4E1D4C","#3FB1CE")
	                		col = colors[randomNum(0,6)]
	                		for(var k in data['res'])
	                		{
	                			var popup = new mapboxgl.Popup({ offset: 25 }).setText(
									name.value+': '+data['res'][k][2].toString()+' IP address'
									);
	                			var marker = new mapboxgl.Marker({color:col})
								  .setLngLat([data['res'][k][1], data['res'][k][0]])
								  .setPopup(popup)
								  .addTo(map);
	                		}
	                	}
	                }
	                });
				}