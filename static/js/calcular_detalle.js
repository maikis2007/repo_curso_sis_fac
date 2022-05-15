function calcular_detalle() { // Calcular el Detalle

    var cantidad,precio,descuento,subtotal,total;

    cantidad = $("#id_cantidad_detalle").val();
    precio = $('#id_precio_detalle').val();
    descuento = $('#id_descuento_detalle').val();

    // Mismas Comprobaciones hasta Descuento

    cantidad = cantidad === "" ? 0 : cantidad;
    cantidad = cantidad < 0 ? 0 : cantidad;

    precio = precio === "" ? 0 : precio;
    precio = precio < 0 ? 0 : precio;

    descuento = descuento === "" ? 0 : descuento;
    descuento = descuento < 0 ? 0 : descuento;

    // Comprobación del Descuento

    descuento = descuento >= (cantidad * precio) ? 0 : descuento;

    // Luego de las Comprobaciones, vienen las Afirmaciones
    
    subtotal = cantidad * precio;
    total = subtotal - descuento;

    // Mostrar datos calculados

    $("#id_catidad_detalle").val(cantidad);
    $("#id_precio_detalle").val(precio);
    $("#id_descuento_detalle").val(descuento);
    $("#id_sub_total_detalle").val(subtotal);
    $("#id_total_detalle").val(total);

}

$(function () {
    $("#id_cantidad_detalle, #id_precio_detalle, #id_descuento_detalle").change( function () {
        calcular_detalle();
    });
});
