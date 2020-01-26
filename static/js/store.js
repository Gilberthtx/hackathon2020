var total = 0
if(document.readyState == 'loading'){
    document.addEventListener('DOMContentLoaded', ready)
} else{
    ready()
}
function ready(){
    var removeItemFromCartButtons = document.getElementsByClassName("btn-remove")
    for(var i = 0; i < removeItemFromCartButtons.length; i++){
        var button = removeItemFromCartButtons[i]
        button.addEventListener('click', removeItemFromCart)
    }

    var addToCartButtons = document.getElementsByClassName('addButton')
    for(var i = 0; i < addToCartButtons.length; i++){
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }
}


$(".shopping-button").click(function(){
    $(".checkout").toggle();
});

$(".check-out-button").click(function(){
    $(".payment").toggle();
});

$(".payment-button").click(function(){
    $(".payment").toggle();
});



function removeItemFromCart(){
     var buttonClicked = event.target
     console.log(buttonClicked)
     var cartItems = document.getElementsByClassName('cart-items')
     var itemPrice = document.getElementsByClassName('cart-item-price')[0].innerText
     itemPrice = parseFloat(itemPrice.replace("$", ""))
     total = total - itemPrice
     document.getElementsByClassName('totalPrice')[0].innerText = ("The Total Cost: $" + total)
     buttonClicked.parentElement.parentElement.remove()
}

function addToCartClicked(event) {
    var button = event.target
    var shopItem = button.parentElement
    var title = shopItem.getElementsByClassName('meal-title')[0].innerText
    var itemPrice = shopItem.getElementsByClassName('item-price')[0].innerText
    var imageSourceForItem = shopItem.getElementsByClassName('item-images')[0].src
    console.log(title, itemPrice, imageSourceForItem)
    addItemToCart(title, itemPrice, imageSourceForItem)
}

function addItemToCart(title, itemPrice, imageSourceForItem) {
    var cartRow = document.createElement('div')
    var cartItems = document.getElementsByClassName('cart-items')[0]
    var cartRowContent = `
                <div class = "cart-items">
                    <div class="inside-cart">
                        <img class= "cart-img" src="${imageSourceForItem}">
                        <span class ="cart-item-title"> ${title}</span>
                        <span class ="cart-item-price"> ${itemPrice}</span>
                        <button class="btn-remove btn btn-warning" type="button">REMOVE</button>
                     </div>
                </div>`
    cartRow.innerHTML = cartRowContent
    cartItems.append(cartRow)
    alert(title + " Has been added to the cart!")
    var realItemPrice = parseFloat(itemPrice.replace("$", ""))
    console.log(realItemPrice)
    addToCartTotal(realItemPrice)
    cartRow.getElementsByClassName('btn-remove')[0].addEventListener('click', removeItemFromCart)
}

function addToCartTotal(price) {
    var addedPrice = price
    total = total + price
    document.getElementsByClassName('totalPrice')[0].innerText = ("The Total Cost: $" + total);
}
