$(document).ready(function() {
	// Source: Pretty Printed

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				query : $('#query').val(),
				latitude : $('#latitude').val(),
                longitude : $('#longitude').val()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				CreateTableFromJSON(data);
				$('#errorAlert').hide();
			}

		});

		event.preventDefault(); // prevents form from submitting twice

	});

});

function CreateTableFromJSON(json_data) {
	// Source: https://www.encodedna.com/javascript/populate-json-data-to-html-table-using-javascript.htm
	// EXTRACT VALUE FOR HTML HEADER.
	var col = ["name", "latitude", "longitude", "population", "score"];

	// CREATE DYNAMIC TABLE.
	var table = document.createElement("table");

	// CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

	var tr = table.insertRow(-1);                   // TABLE ROW.

	for (var i = 0; i < col.length; i++) {
		var th = document.createElement("th");      // TABLE HEADER.
		th.innerHTML = col[i];
		tr.appendChild(th);
	}

	// ADD JSON DATA TO THE TABLE AS ROWS.
	for (var i = 0; i < json_data.length; i++) {

		tr = table.insertRow(-1);

		for (var j = 0; j < col.length; j++) {
			var tabCell = tr.insertCell(-1);
			tabCell.innerHTML = json_data[i][col[j]];
		}
	}

	// FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
	var divContainer = document.getElementById("showData");
	divContainer.innerHTML = "";
	divContainer.appendChild(table);
}
