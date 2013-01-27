$(document).ready(function() {
    
    var $subBox = $("#selected-light > tr");
    
    //选中单个任务的行为
    $subBox.find("input:checkbox").click(function() {
        var id = '#' + $(this).attr("id");
		$(id).toggleClass("info");
        
        if ($subBox.length == $("#selected-light").find('input:checkbox:checked').length) {
            $("#all").attr("checked", true);
        } else {
            $("#all").attr("checked", false);
        }
        
        if ($("#selected-light").find('input:checkbox:checked').length == 0) {
            $("#btn-hide").hide();
        } else {
        	$("#btn-hide").show();
        }
    })
    
    //选中所有任务的行为
    $("#all").click(function() {
        $("#selected-light").find('input:checkbox').attr('checked', this.checked);
        
        if (this.checked == true) {
            $("#selected-light").find("tr").addClass("info");
        	$("#btn-hide").show();
        } else {
            $("#selected-light").find("tr").removeClass("info");
			$("#btn-hide").hide();
        }
    })
    
    //如果复选框和任务默认情况下是选择的，则高亮
    $('#selected-light > tr:has(:checked)').addClass("info");
    
    if ($("#selected-light").find('input:checkbox:checked').length != 0) {
    	$("#btn-hide").show();
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
    
    //输入框获得焦点时，弹出输入列表并获取保存的内容
    $('.add_input').focus(function() {
    	var post = $('.add_input').offset();
    	var width = $('.add_input').width();
    	var left_post = post.left + width + 18;
    	$(this).val($('#input_list .active').find('.text').text())
    	$('#input_list').css({'max-width':'480px','width':'auto','top':'4px','left':left_post + 'px'});
    	$('#input_list').show();	
    	
    	autoc($('#input_list').find('.active'));
    })
    
    //监视失去焦点，回车，TAB事件，保存用户的输入
    function save_text () {
        var $input_list = $('#input_list .active').find('.text');
    	$input_list.text($('.add_input').val());
    	var id = $('#input_list .active').attr('index');
    	$("#" + id).val($('.add_input').val());
    }
    
    $('.add_input').blur(save_text);
    $('.add_input').keydown(function(event){
    	if (event.which == 13) {
    		save_text();
    	}
    })
    
    //监视键盘的TAB键的事件，用来切换输入列表
    $('.add_input').keydown(function(event) {	
    	var $input_list = $('#input_list .active')
    	if (event.which == 9) {
    		event.preventDefault(); 
    		save_text(); 				
		    $input_list.removeClass('active');
			if ($input_list.next().length > 0) {
			    $input_list.next().addClass('active');
			    $(this).val($input_list.next().find('.text').text());
			    autoc($input_list.next());
			} else {
			    $('#input_list').find('li').first().addClass('active');
			    $(this).val($('#input_list').find('li').first().find('.text').text());
			    autoc($('#input_list').find('li').first());
			}
    	}
    })
    
    //点击外部区域隐藏输入列表
    var $set = $("*").not('.add_input').not('#input_list')
    var $input_list = $('#input_list *')
    
    $input_list.each(function(){
    	$set = $set.not(this);
    })
    
    $set.click(function() {
    	$('.add_input').val(null);
    	$('#input_list').hide();
    })

    //阻止事件的冒泡
    $('#input_list').click(function(event) {
    	event.stopPropagation();
    })
    
    $('.add_input').click(function(event) {
    	event.stopPropagation();
    })
    
    //添加一个任务成功后，任务输入框默认获得焦点,并高亮新任务
    if ($subBox.hasClass("new")) {
    	$('.new').css('background-color','#FFDBA5');
    	$('.add_input').focus();
    }
    
    // 根据切换到的输入列表弹出自动完成，并获取数据源
    function autoc ($item) {
    	var post = $('.add_input').offset();
    	var height = $('.add_input').height();
    	var left_post = post.left;
    	var top_post = height + 15;
    	
    	if (($item.attr('index') == 'task_list') || ($item.attr('index') == 'priority')) {
    		if ($item.attr('index') == 'task_list') {
    			$('.autoc').html($('.task_list').html());
    		} else {
    			$('.autoc').html($('.priority').html());
    		}
    		$('.autoc').css({'top': top_post + 'px', 'left':left_post + 'px'});
    		$('.autoc').show();
    		$('.add_input').attr('readonly', 'readonly');
    	} else {
    		$('.autoc').hide();
    		$('.add_input').removeAttr('readonly');
    	}
    	
    	//初始化默认选中的项目
    	$('.autoc > li').each(function () {
    		if ($(this).attr('data-value') == $('.add_input').val()) {
    			$(this).addClass('active');		
    		}
    	})
    }
    
    //输入框失去焦点时候，隐藏自动完成
    $('.add_input').blur(function() {
    	$('.autoc').hide();
    	$('.add_input').removeAttr('readonly');
    })
    
    //监视上下键事件，切换自动完成的选项
    $('.add_input').keydown(function(event) {
    	var $active = $('.autoc .active')
    	
    	if ((event.which == 75) && ($('.autoc').is(':visible') == true)) {
    		event.preventDefault(); 
    		$active.removeClass('active');
    		if ($active.next().length > 0) {
    			$active.next().addClass('active');
    		} else {
    			$('.autoc').find('li').first().addClass('active');
    		}
    	}
    	
    	if ((event.which == 73) && ($('.autoc').is(':visible') == true)) {
    		event.preventDefault();
    		$active.removeClass('active');
    		if ($active.prev().length > 0) {
    			$active.prev().addClass('active');
    		} else {
    			$('.autoc').find('li').last().addClass('active');
    		}
    	}
    })
    
    //监视回车事件，提交数据和提交表单
    $('.add_input').keydown(function(event) {
    	if ((event.which == 13) && ($('.autoc').is(':visible') == true)) {
    		if ($('.add_input').val() == $('.autoc .active').attr('data-value')) {
    			var names = $('#submib_addtask').attr("name");
        		$("#submib_value").attr('name', names);
        		$("#edit_list").submit();
    		} else {
    			event.preventDefault(); 
    			$('.add_input').val($('.autoc .active').attr('data-value'));
    			save_text();
    		}
    	}
    })
    
})
