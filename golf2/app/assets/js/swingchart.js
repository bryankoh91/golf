function drawXYChart(users, xyChartData) {
	const config = {
		type: 'line',
		data: {
			datasets: []
		},
		options: {
			scales: {
				x: {
					type: 'time',
					time: {
						parser: 'yyyy-MM-dd HH:mm:ss',
						unit: 'minute',
						displayFormats: {
							minute: 'dd MMM HH:mm'
						}
					}
				} //end of x-axis
			} //end of scales
		} //end of options
	}; //end of config

	var myChart = new Chart(document.getElementById('swingChart'), config);

	for (var i = 0; i < users.length; i++) {
		var newDataset = {
			label: users[i],
			data: xyChartData[i],
			borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
			backgroundColor: 'rgba(249, 238, 236, 0.74)', 			
		};

		myChart.data.datasets.push(newDataset);
	}

	myChart.update();

} //end of drawXYChart

$.ajax({
    url: "/swingchart",
    method: "POST",
    data:{
        start: 0000,
        end: 9999
    },
    error: function(){
        alert("Error");
    },
    success: function(data, status, xhr){
        
		var users = [];
		var xyChartData = [];

		for (const [key, values] of Object.entries(data.xyData)) {
			users.push(key);
			var xy = [];
			for (var i = 0; i < values.length; i++) {
				xy.push({x: values[i][0], y: values[i][1]})
			}
			xyChartData.push(xy);
		}

		drawXYChart(users, xyChartData);
		
    } //end of success

}) //end of ajax