function register(){
		if (document.getElementById('passwd').value != document.getElementById('repasswd').value){
 	  		alert('两次密码不相同')
 	  		return
 	  	}
		d = {}
		d['username'] = document.getElementById('username').value
		d['password'] = document.getElementById('passwd').value
		d['name'] = document.getElementById('name').value
		d['email'] = document.getElementById('email').value
		d['college'] = document.getElementById('college').value
		d['department'] = document.getElementById('department').value
		d['identity'] = document.getElementById('identity').value
		d['mobile'] = document.getElementById('mobile').value
		d['address'] = document.getElementById('address').value
		d['postcode'] = document.getElementById('postcode').value
		$.ajax({
			type:"POST",
			url:"/userregister",
			data: d,
			success:function reg_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			alert(result['message'])
 	  			window.location = '/'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }
 	  
 	  function login(){
 	  	d = {}
 	  	d['username'] = document.getElementById("username").value
 	  	d['password'] = document.getElementById("passwd").value
 	  	$.ajax({
			type:"POST",
			url:"/userlogin",
			data: d,
			success:function login_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			setCookie('useridthu', result['userid'], 1)
 	  			setCookie('usernamethu', result['username'], 1)
 	  			setCookie('tokenthu', result['token'], 1)
 	  			window.location = '/mainpage'
 	  		}
 	  		else{
 	  			alert(result['message'])
 	  		}
 	  	}
		})
 	  }

 	  function checklogin(){
 	  	d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')

 	  	$.ajax({
			type:"POST",
			url:"/userchecklogin",
			data: d,
			success:function checklogin_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			//document.getElementById('mainframe').style.display = ''
 	  		}
 	  		else{
 	  			alert('请先登录')
 	  			window.location = '/'
 	  		}
 	  	}
		})
 	  }

 	  function showuserinfo(){
 	  	d = {}
 	  	d['userid'] = getCookie('useridthu')
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	$.ajax({
			type:"POST",
			url:"/getuserinfo",
			data: d,
			success:function userinfo_return(data){
 	  		result = JSON.parse(data)
 	  		if (result['success'] == 1){
 	  			document.getElementById('username').innerHTML=result['username']
 	  			document.getElementById('name').innerHTML=result['name']
 	  			document.getElementById('email').innerHTML=result['email']
 	  			document.getElementById('college').innerHTML=result['college']
 	  			document.getElementById('department').innerHTML=result['department']
 	  		}
 	  		else{
 	  		}
 	  	}
		})
 	  }

 	  function logout(){
 	  	d = {}
 	  	d['username'] = getCookie('usernamethu')
 	  	d['token'] = getCookie('tokenthu')
 	  	delCookie('usernamethu')
 	  	delCookie('useridthu')
 	  	delCookie('tokenthu')
 	  	jsondata = JSON.stringify(d)
 	  	$.post('/logout/'+jsondata)
 	  	window.location = '/'
 	  }

 	  function modify(){
 	  	d = {}
 	  	d['username'] = getCookie('username')
 	  	d['name'] = document.getElementById('namem').value
 	  	d['token'] = getCookie('token')
 	  	jsondata = JSON.stringify(d)
 	  	$.post('/modify/'+jsondata,
 	  		function modifyre(data){
 	  			result = JSON.parse(data)
 	  			document.getElementById('LayerModify').style.display = 'none'
 	  			if (result['success'] == 1)
 	  				setCookie('truename', document.getElementById('namem').value, 1)
 	  			alert(result['message'])
 	  		}
 	  	)
 	  }

 	  function modifypassword(){
 	  	if (document.getElementById('newpass').value != document.getElementById('renewpass').value){
 	  		alert('两次密码不相同')
 	  		return
 	  	}
 	  	d = {}
 	  	d['username'] = getCookie('username')
 	  	d['oldpass'] = $.md5(document.getElementById('oldpass').value)
 	  	d['newpass'] = $.md5(document.getElementById('newpass').value)
 	  	d['token'] = getCookie('token')
 	  	jsondata = JSON.stringify(d)
 	  	$.post('/modifypassword/'+jsondata,
 	  		function modifyre(data){
 	  			result = JSON.parse(data)
 	  			if (result['success'] == 1){
 	  				document.getElementById('oldpass').value = ''
 	  				document.getElementById('newpass').value = ''
 	  				document.getElementById('renewpass').value = ''
 	  				document.getElementById('LayerModifypassword').style.display = 'none'
 	  			}
 	  			alert(result['message'])
 	  		}
 	  	)
 	  }