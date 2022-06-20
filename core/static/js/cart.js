let btns = document.getElementsByClassName('add-to-cart')
for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action
        location.reload()

        if (user === "AnonymousUser") {
            console.log("User is not logged in")
        } else {
            updateCart(productId, action)
        }
    })
}

function updateCart(id, action) {
    let url = '/updatecart'
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',

        },
        body: JSON.stringify({'productId': id, 'action': action})
    })
        .then(response => response.json())
        .then(data => console.log(data))
}

let quantityField = document.getElementsByClassName('cart_quantity_input')
for (let i = 0; i < quantityField.length ; i++) {
    quantityField[i].addEventListener('change', function (){
        let quantityFieldValue = quantityField[i].value
        let quantityFieldProduct = quantityField[i].parentElement.parentElement.children[1].children[0].innerText

        let url = '/updatquantity'
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken-Type': csrftoken,
                'Content-Type': 'application/json'
            }
        })
    })
}