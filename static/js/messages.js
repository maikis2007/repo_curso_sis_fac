function mensaje(msg, color='green') {
    if (color == 'success'){
        color = 'green';
    } else if (color == 'info'){
        color = 'orange';
    } else if (color == 'error'){
        color = 'red';
    }

    $.alert({
        title: '',
        theme: 'material',
        type: color,
        content: msg
    });
}
