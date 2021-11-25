function abrir_modal(url){
    $("#popup").load(url, function(){
        $(this).modal({
            backdrop: 'static',
            keyboard: false
        })
        $(this).modal('show');
    });
    return false;
}

function cerrar_modal(){
    $("#popup").modal('hide');
    return false;
}
