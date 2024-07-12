const nav = $('nav')

async function setNavLinks() {
    const res = await axios.get('/login-state')
    const ul = nav.children()
    if (res.data["logged-in"] == true) {
        for (let li of ul.children()) {
            if (li.classList.contains('logged-out')) {
                li.style.display = 'none';
            }
        }
    } else{
        for (let li of ul.children()) {
            if (li.classList.contains('logged-in')) {
                li.style.display = 'none';
            }
        }
    }
}

setNavLinks()
