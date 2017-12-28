		function checkData_form(){  //检查form表单数据的合法性
			var index = true;
			var username = $("input[name='username']").val();
			var password = $("input[name='password']").val();
			$("input").css("border-color", "#ddd");
			if(username == ""){
		    	index = false;
		    	$("input[name='username']").attr("placeholder","please enter username!");
		    	$("input[name='username']").attr("style","::placeholder:red")
			} 
			if(password == ""){
		    	index = false;
		    	$("input[name='password']").css("border-color", "#f33");
			}
			return index
			}
		function checkLogin(){
			var verifyInput = checkData_form();
			if (verifyInput == true){
				var username = $("input[name='username']").val();
				var password = $("input[name='password']").val();
				data = {'userNo':username, 'passwd':password}
				postRequest("/verifyLogin/",data,true,verifyResult);
			}else {
				alert("username or password is not should null!")
			}
		}
		function verifyResult(ret){
			if(ret['result'] == true) {
				window.location.href = "/index/"+ret['sessionId'];
			}else {
				alert(ret['error']);
			}

		}
		$(function () {
			$("input[name = 'username']").keydown(function(event){  
    			if(event.which == "13")      
            		$("input[name = 'password']").focus() 
			})
			$("input[name = 'password']").keydown(function(event){  
    			if(event.which == "13")      
            		checkLogin(); 
			})
			$("input[name = 'submit']").click(function(){
				checkLogin();
			});
		})