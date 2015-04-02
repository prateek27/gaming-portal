var myUrl = 'http://127.0.0.1:8000/user-graph/';
var req = new XMLHttpRequest();

var displayStatus = (function(){
	return{
		init: function(){
			var usernameBox = document.getElementById('id_username');
			var enteredUsername = usernameBox.value;
			var statusBox = document.getElementById('live_status_container');


			statusBox.addEventListener('focusout', function(e){
				e.preventDefault();

				function fetch(e){
					var usernameList = this.response.fields
					print(usernameList)
				}
				
				req.open("GET", myUrl, true);
				req.responseType = 'json';
				req.addEventListener('load', fetch);
				req.send();


			});


		}
	};
})();

