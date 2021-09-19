productQuantity.forEach((number, index) => {
                    
    number[index].innerHTML = response.items[index].fields.quantity
    if (response.items[index].fields.product){
        alert('hey')
    }else{
        alert('na')
    }
    number[index].innerHTML = response.productPrice[index]
    if (!response.items[index].fields.quantity){
        //document.querySelectorAll('.productTotal')[index]
        alert('hello')
    }
    //console.log('fefewfwfw',document.querySelectorAll('.productTotal')[index])
})      