function abrir_modal(url){
    $("#popup").load(url, function(){
        $(this).modal({
            keyboard: false
        })
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal(url){
    $("#popup").modal('hide');
    return false;
}
