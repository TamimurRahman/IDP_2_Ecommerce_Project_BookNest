$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log('data = ',data);
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount
        }
    })
})
$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log('data = ',data);
            eml.innerText=data.quantity
            document.getElementById('amount').innerText=data.amount
            document.getElementById('totalamount').innerText=data.totalamount
        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var itemRow = $(this).closest('.row');  // Get the entire cart row

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function (data) {
            itemRow.remove();  // Remove the item from the UI
            document.getElementById('amount').innerText = "Tk. " + data.amount;
            document.querySelector('li:nth-child(2) span').innerText = "Tk. " + data.shipping;
            document.getElementById('totalamount').innerText = "Tk. " + data.totalamount;

            if (data.cart_empty) {
                location.reload();  // Or show "Cart is Empty" message
            }
        }
    });
});

$('.plus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();

    $.ajax({
        type: "GET",
        url: "/pluswishlist/",
        data: {
            prod_id: id
        },
        success: function (data) {
            alert(data.message);  // or update the UI dynamically
            window.location.reload();  // Optional: reload page to reflect wishlist change
        }
    });
});
$('.minus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();

    $.ajax({
        type: "GET",
        url: "/minuswishlist/",
        data: {
            prod_id: id
        },
        success: function (data) {
            alert(data.message);  // or update the UI dynamically
            window.location.reload();  // Optional: reload page to reflect wishlist change
        }
    });
});
