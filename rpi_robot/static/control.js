$("#reboot_id").click(function(){
    $.post("/control",{'reboot':'reboot'})

});

$("#mv_left").click(function(){
    $.post("/control/mv", {move:"left"})
});

$("#mv_right").click(function(){
    $.post("/control/mv", {move:"right"})
});

$("#mv_forward").click(function(){
    $.post("/control/mv", {move:"forward"})
});

$("#mv_backward").click(function(){
    $.post("/control/mv", {move:"backward"})
});

$("#cam_backward").click(function(){
    $.post("/control/cam", {move:"backward"})
});

$("#cam_forward").click(function(){
    $.post("/control/cam", {move:"forward"})
});

$("#led_text_button_id").click(function(){
    
    var value=$("#led_text_id").val()
    $.post('/control/led',{'type':'text_display',
            'data':value})
});

$('#led_temp_button_id').click(function(){
    var value=$('#led_temp_text_id').val()
    $.post('/control/led',{'type':'temp_display',
                    'data':value})
    
});

$('.emojiClass').click(function(e){
   var data=e.target.id
   $.post('/control/led',{'type':'emoji_display','data':data})
    
});


$("#led_stop_id").click(function(){
    $.post("/control/led",{'type':'stop_led'})
});
