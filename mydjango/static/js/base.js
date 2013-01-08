$(document).ready(function() {
    
    var $subBox = $("#selected-light > tr");
    
    //选中单个任务的行为
    $subBox.click(function() {
        $(this).toggleClass("info");
        
        if ($(this).hasClass("info")) {
        	$(this).find("input:checkbox").attr("checked", true);
        } else {
        	$(this).find("input:checkbox").attr("checked", false);
        }
        
        if ($subBox.length == $("#selected-light").find('input:checkbox:checked').length) {
            $("#all").attr("checked", true);
        } else {
            $("#all").attr("checked", false);
        }
        
        if ($("#selected-light").find('input:checkbox:checked').length == 0) {
            $("#btn-hide").each(function() {
                $(this).hide();
            })
        } else {
            $("#btn-hide").each(function() {
                $(this).show();
            })
        }
    })
    
    //选中所有任务的行为
    $("#all").click(function() {
        $("#selected-light").find('input:checkbox').attr('checked', this.checked);
        
        if (this.checked == true) {
            $("#selected-light").find("tr").addClass("info");
            $("#btn-hide").each(function() {
                $(this).show();
            })
        } else {
            $("#selected-light").find("tr").removeClass("info");
            $("#btn-hide").each(function() {
                $(this).hide();
            })
        }
    })
    
    //如果复选框和任务默认情况下是选择的，则高色
    $('#selected-light > tr:has(:checked)').addClass("info");
    
    if ($("#selected-light").find('input:checkbox:checked').length != 0) {
        $("#btn-hide").each(function() {
            $(this).show();
        })
    }
    
    //下拉菜单使用链接提交表单
    $(".dropdown-menu").find("a").click(function() {
        var names = $(this).attr("name");
        var values = $(this).attr("value");
        $("#submib_value").attr('name', names);
        $("#submib_value").attr('value', values);
        $("#edit_list").submit();
    })
    
    //显示并延时20秒关闭消息提示
    var widths = $(".myalert").width();
    var widths = widths / 2 ;
    $(".myalert").css("margin-left", "-" + widths + "px");
    
    if ($(".alert").attr("state") == "show") {
        $(".alert").show();
        
        setTimeout(function() {
        	$(".alert").alert('close');
    	}, 20000);
    }
    
    //同步新增工具栏和列表的宽度
    var widths = $("#selected-light").width();
    $(".button_nav").css("width", widths + "px");
    
    //页面载入时，设置输入列表的位置 和大小

    
    //输入框获得焦点时，弹出输入列表 
    $('.add_input').focus(function() {
    	var post = $('.add_input').offset();
    	var width = $('.add_input').width();
    	var left_post = post.left + width + 18;
    	$('#input_list').css({'width':'480px', 'top':'4px', 'left': left_post + 'px'});
    	$('#input_list').show();	
    })
    
    //输入框失去焦点时，隐藏输入列表 
    $('.add_input').blur(function() {
    	$('#input_list').hide();
    })
    
    //监视键盘的TAB键的事件，用来切换输入列表
    $('.add_input').keydown(function(event) {	
    	var $input_list = $('#input_list .active')
    	if (event.which == 9){
    		event.preventDefault();
    		$input_list.removeClass('active');
	    	if ($input_list.next().length > 0) {
	    		$input_list.next().addClass('active');
	    	} else {
	    		$('#input_list').find('li').first().addClass('active');
	    	}
    	}
    	
    })

})
