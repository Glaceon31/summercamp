
function getapplylist(){
	d = {}
 	d['userid'] = getCookie('useridthu')
 	d['username'] = getCookie('usernamethu')
 	d['token'] = getCookie('tokenthu')
 	var applylist = []
 	$.ajax({
			type:"POST",
			url:"/getapplylist",
			data: d,
			async:false,
			success:function getapplylist_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			applylist = result['applylist']
 	  		}
 	  		else{
 	  		}
 	  	}
	})
	return applylist
}

function apply_submit(){
	d = {}
 	d['userid'] = getCookie('useridthu')
 	d['username'] = getCookie('usernamethu')
 	d['token'] = getCookie('tokenthu')
 	d['title'] = document.getElementById('activity').value
 	var usernameinput = $("<input>").attr("type", "hidden").attr("name", "username").val(getCookie('usernamethu'));
 	$('#applyform').append($(usernameinput))
 	var tokeninput = $("<input>").attr("type", "hidden").attr("name", "token").val(getCookie('tokenthu'));
 	$('#applyform').append($(tokeninput))
 	var useridinput = $("<input>").attr("type", "hidden").attr("name", "userid").val(getCookie('useridthu'));
 	$('#applyform').append($(useridinput))
 	var titleinput = $("<input>").attr("type", "hidden").attr("name", "title").val(getCookie(document.getElementById('activity').value));
 	$('#applyform').append($(titleinput))
 	a = $('#applyform').submit()

 	/*
 	$.ajax({
			type:"POST",
			url:"/submit",
			data: $('#applyform').serialize(),
			success:function apply_submit_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert('提交成功')
 	  			window.location = '/mainpage'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
	})*/
}

function apply_cancel(){
	d = {}
 	d['userid'] = getCookie('useridthu')
 	d['username'] = getCookie('usernamethu')
 	d['token'] = getCookie('tokenthu')
 	d['title'] = document.getElementById('applies').value
 	$.ajax({
			type:"POST",
			url:"/cancel",
			data: d,
			success:function apply_cancel_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert('取消成功')
 	  			window.location = '/mainpage'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
	})
}