
var updateLogin_Logout = document.getElementsByClassName('updateLogin_Logout')
var updateUserStatus = document.getElementsByClassName('name-user')

if (user === "AnonymousUser")
{
    updateUserStatus[0].classList.add('hiden-name-user')

    for (i = 0; i < updateLogin_Logout.length; i++)
    {
        updateLogin_Logout[i].classList.remove('hiden-login-logout')
    }
}
else
{
    updateUserStatus[0].classList.remove('hiden-name-user')

    for (i = 0; i < updateLogin_Logout.length; i++)
    {
        updateLogin_Logout[i].classList.add('hiden-login-logout')
    }

}   

//
//
//
//  CART 
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action

        if (user === "AnonymousUser") {
            console.log('Nguoi dung chua dnag nhap')
        }
        else {
            updateUserOrder(productId, action)
        }
        
    })
}


function updateUserOrder(productId, action) {
    var url = '/update_item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        // console.log('data', data)
        location.reload()
    })
}