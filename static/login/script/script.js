function hide() {
    let eye = document.getElementById('shaha')
    pass = document.querySelector('.pass')
    eye.addEventListener('click', () => {
        if (pass.type === 'password') {
            pass.type = 'text'
            eye.classList.remove('fa-eye')
            eye.classList.add('fa-eye-slash')
        } else if (pass.type === "text") {
            pass.type = 'password'
            eye.classList.remove('fa-eye-slash')
            eye.classList.toggle('fa-eye')
        }
    })
}

hide()