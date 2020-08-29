jQuery(document).ready(function(){
	addEvents();	
});


var previous_team = "0";
var datatable;

function addEvents() {
	var team_id;
	$('.content-wrapper').on('change','#team',teamChanged);
}










function teamChanged() {
	var value = $(this).val()
	match_id = value;
	var is_changing_allowed = true;
	if(previous_team != "0"){
		if (confirm('Are you sure you want to change team?')) {
    		is_changing_allowed = true;
		} else {
		    is_changing_allowed = false;
		}
	}
	if (value != "0" && is_changing_allowed){
		var form_data = new FormData()
		form_data.set('csrfmiddlewaretoken',getCookie('csrftoken'));
		form_data.set('team',value);
		var url = '/cricket/team_match_point/'
		ajaxCall(form_data,url,TeamPointList,displayError);
	}
	else if(is_changing_allowed){
		previous_team = "0";
		emptyStudentList	
	}
}



function ajaxCall(data,url,successHandler,ErrorHandler) {
	$.ajax({
		type : 'POST',
		url : url,
		data : data,
		contentType : false,
		processData : false,
		success : function(response){
			successHandler(response)
		},
		error:function(response){
					var x = $("#snackbar");
                    x.html("Error Occured please Try Again or Consult MAAZ!!!!!");
                    x.addClass( "show");
                    setTimeout(function(){ x.removeClass( "show" ).addClass( "" ); }, 1000);
		},
	})
}



function TeamPointList(response) {
	// console.log(html)
	$('#points_list').html(response.html);
	var b =$('#team')
	var team_name = $('#team').find('[value="'+b.val()+'"]').text()
	datatable=$('#points_list').DataTable(
		{
			"dom": '<"top"lBf>rt<"bottom"ip><"clear">',
			"scrollX": true,
			"pageLength": 100,
			"aLengthMenu": [[10, 25, 50, 100], ["10 Per Page", "25 Per Page", "50 Per Page", "100 Per Page"]],
        	buttons: [
            {
                extend: 'print',
                exportOptions: {
                columns: ':visible'
                }
            },'colvis'
        ],
        }
        
		);
	previous_team = response.team


	datatable.on('click','button.btn.btn-primary.payment-info',function(){
	$(this).parents('td').find('.popover').css('opacity','1');
	});
}


function emptyStudentList() {
	// console.log(html)
	$('#points_list').html('')

}

function displayError(message) {
	// body...
}


var getCookie = function(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie).replace(/ /g,'');
    var cookies_list = decodedCookie.split(';');
    for(var i = 0; i <cookies_list.length; i++) {
        cookie = cookies_list[i].split('=')
        if (cookie[0] == cname)
            return cookie[1]
    }
    return "";
}
