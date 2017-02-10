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

