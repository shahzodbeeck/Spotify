let inputss1 = document.querySelector('.mad_elements_bottom_top_input_file'),
    rasmcha = document.querySelector('.rasmcha'), addd = document.querySelector('.section_center_top_h2'),
    cance = document.querySelector('.cancel'), mad = document.querySelector('.madalni')
addd.addEventListener('click', () => {
    console.log('s')
    mad.style.display = `flex`
    mad.style.opacity = `1`

})
cance.addEventListener('click', () => {
    mad.style.display = `none`
    mad.style.opacity = `0`

})
inputss1.addEventListener('change', () => {
    let file = inputss1.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        rasmcha.src = `${content}`
        rasmcha.style.opacity = `1`
    }
    reader.readAsDataURL(file);

});
