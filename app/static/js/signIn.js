$(function(){
	$('#btnSignIn').click(function(){

		$.ajax({
			url: '/validateUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});