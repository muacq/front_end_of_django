$(document).ready(function(){
	$.post("/cat/getAll",{},function(data,status){
		alert(data)
	});
});

