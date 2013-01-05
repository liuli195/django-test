$(document).ready(function(){
	
	var $subBox = $("#selected-light").find("input:checkbox");
	
    $subBox.click(function(){
		var id = '#' + $(this).attr("id");
		$(id).toggleClass("info");
		
		if($subBox.length == $("#selected-light").find('input:checkbox:checked').length){
			$("#all").attr("checked", true);
		}else{
			$("#all").attr("checked", false);
		}
		
		if($("#selected-light").find('input:checkbox:checked').length == 0){
			$("#btn-hide").each(function() {
				$(this).hide();
			})
		}else{
			$("#btn-hide").each(function() {
				$(this).show();
			})
		}
	})
    
    $("#all").click(function(){ 	
    	$("#selected-light").find('input:checkbox').attr('checked', this.checked);
    	
    	if(this.checked == true){
    		$("#selected-light").find("tr").addClass("info");
    		$("#btn-hide").each(function() {
				$(this).show();
			})
    	}else{
    		$("#selected-light").find("tr").removeClass("info");
    		$("#btn-hide").each(function() {
				$(this).hide();
			})
    	}
    	
    })
    
    $('#selected-light > tr:has(:checked)').addClass("info");
    
    if($("#selected-light").find('input:checkbox:checked').length != 0){
    	$("#btn-hide").each(function() {
    		$(this).show();
    	})
    }
    
    $(".dropdown-menu").find("a").click(function(){
    	var names = $(this).attr("name");
    	var values = $(this).attr("value");
    	$("#submib_value").attr('name', names);
    	$("#submib_value").attr('value', values);
    	$("#edit_list").submit();
    })
    
    var widths = $(".myalert").width()
    var widths = widths/2
    $(".myalert").css("margin-left", "-" + widths +"px");
    
    /*$(".alert").alert('close');*/

})
