$(document).ready(function (){
    $('.add-to-cart').on('click', function(e){
        e.preventDefault()
        let productId = $(this).attr('data-productId');
        $.ajax({
            url: '/add-to-cart',
            headers : {
                'X-CSRFToken': csrftoken,
            },
            data: {
                'id': productId,
            },
            dataTypes: 'json',
            method: 'POST'
        })
    })
})