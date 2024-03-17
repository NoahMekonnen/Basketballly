
const loginForm = $('#login-form')
const nav = $('nav')

async function loggedIn() {
    const res = await axios.get('/login-state')
    if (res.data["logged-in"] == "true") {
        for (let link of nav.children()) {
            if (link.id == 'login-link') {
                link.remove()
            }
        }
        const username = await axios.get('/username')
        console.log(username,"Username")
        const logoutLink = $(`<a href= "/${username.data.username}/logout"></a>`).text('Logout')
        console.log(logoutLink,"Logout link")
        // logoutLink.attr("href","/${username.data.username}/logout")
        logoutLink.on('click', function(){
            console.log('hi')
        })
        nav.prepend(logoutLink)
        console.log(nav.children(),"Children")
    }
}

loggedIn()
