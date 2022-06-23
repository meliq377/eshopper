$(document).ready(function () {
    $('.add-to-cart').on('click', function (e) {
        e.preventDefault()
        let productId = $(this).attr('data-productId');
        $.ajax({
            url: '/add-to-cart',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: {
                'id': productId,
            },
            dataTypes: 'json',
            method: 'POST',
            success: function (data) {
                console.log(data)
                alertify.success(data.status)
            }
        })
    })
})

$('.input-number').bind('keyup mouseup', function () {
    let quantity = $(this).val();
    console.log(quantity)
    if (quantity < 0) {
        quantity = 0;
    }
    let product_id = $(this).attr('data-product-id');
    $.ajax({
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        url: 'cart_quantity_update',
        data: {
            quantity: quantity,
            product_id: product_id
        },
        success: function (data) {
            console.log(data)
            $(`.product-${product_id} .cart_total_price`).html(`
                $${data.total}
            `)
        },
        error: function () {
            alertify.error('error')
        },
    })
});


$('body').on('click', '.cart_delete', function () {
    let product_id = $(this).attr('data-product-id');
    $.ajax({
        headers: {
            'X-CSRFToken': csrftoken,
        },
        type: 'POST',
        url: 'cart_quantity_delete',
        data: {
            product_id: product_id
        },
        success: function (data) {
            console.log(data)
            alertify.success(data.status)
            $(`.product-${product_id}`).remove()

        },
        error: function () {
            alertify.error('error')
        },
    })
});