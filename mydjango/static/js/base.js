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
    var widths = $("#selected-light").width()
    $(".add_nav").css("width", widths + "px");
    
    //初始化弹出提示框
    $('.myicon').popover({
    	placement: 'bottom',
    	content: '!优先级<br/>^开始时间',
    	title: '智能添加快捷键',
    	html: true,
    })
})
