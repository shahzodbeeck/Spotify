const inputssds = document.getElementById('imageInput2');
const genre = document.getElementById('genre');
let madall = document.querySelector('.madalni2'), ekssssss = document.querySelector('.cancel2'),
    ras = document.querySelector('.rasmcha2'), inp = document.querySelector('.mad_elements_bottom_top_input2')
inputssds.addEventListener('change', () => {
    const files = inputssds.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        ras.src = `0`
        ras.src = `${content}`
        ras.style.opacity = `1`
    }
    reader.readAsDataURL(files);
})


function uploadImage() {
    const file = inputssds.files[0];
    const formData = new FormData();
    if (file) {
        formData.append('image', file);
    }
    formData.append('name', genre.value);
    formData.append('id', ids);
    fetch('/edit_genre', {
        method: 'POST', body: formData,
    })
        .then(response => response.json())
        .then(data => {
            const table = document.querySelector('.section_center_center')
            table.innerHTML = ``
            let shs = data.result
            madall.style.opacity = '0';
            madall.style.display = 'none';
            shs.forEach((item, id) => {
                table.innerHTML += `    <a href=""><div class="section_center_center_element"
                         data-id="${shs[id].id}" data-photo="${shs[id].photo}" data-name="${shs[id].name}"
                         style="background: rgba(${shs[id].rgba}); position: relative;">

                                <div class="cointener" style="position: absolute;">
                                    <i
                                            class="fa-solid fa-pen pencil"></i>
                                    <a style="text-decoration: none;" href="delete_genre/${shs[id].id}">
                                        <i
                                                class="fa-solid fa-trash-can can"></i></a>
                                </div>

                        <div class="section_center_center_element_top" style="margin-top: 5px;">
                            ${shs[id].name}
                        </div>
                        <div class="section_center_center_element_bottom">
                            <img class="section_center_center_element_bottom_img" style="width: 105px;height: 105px; object-fit: cover; -webkit-transform: rotate(25deg) translate(18%,-2%);
    transform: rotate(25deg) translate(18%,-2%);"
                                 src="${shs[id].photo}">
                        </div>
                    </div></a> 
`;

            })
            const editss = document.querySelectorAll('.pencil');
            const elemetlar = document.querySelectorAll('.section_center_center_element');

            ekssssss.addEventListener('click', () => {
                madall.style.opacity = '0';
                madall.style.display = 'none';
            });

            editss.forEach((item, index) => {
                item.addEventListener('click', () => {
                    madall.style.opacity = '1';
                    madall.style.display = 'flex';
                    ras.src = elemetlar[index].getAttribute('data-photo');
                    ras.style.opacity = '1';
                    inp.value = elemetlar[index].getAttribute('data-name');
                    ids = elemetlar[index].getAttribute('data-id');
                });
            });
        })
}

fetch('/send')
    .then(response => response.json())
    .then(data => {
        const table = document.querySelector('.section_center_center')
        table.innerHTML = ``
        let shs = data.result
        shs.forEach((item, id) => {
            table.innerHTML += `    <a href="genre" style="text-decoration: none;"> 
    <div class="section_center_center_element"
                         data-id="${shs[id].id}" data-photo="${shs[id].photo}" data-name="${shs[id].name}"
                         style="background: rgba(${shs[id].rgba}); position: relative;">

                                <div class="cointener" style="position: absolute;">
                                    <i
                                            class="fa-solid fa-pen pencil"></i>
                                    <a style="text-decoration: none;" href="delete_genre/${shs[id].id}">
                                        <i
                                                class="fa-solid fa-trash-can can"></i></a>
                                </div>

                        <div class="section_center_center_element_top" style="margin-top: 5px;">
                            ${shs[id].name}
                        </div>
                        <div class="section_center_center_element_bottom">
                            <img class="section_center_center_element_bottom_img" style="width: 105px;height: 105px; object-fit: cover; -webkit-transform: rotate(25deg) translate(18%,-2%);
    transform: rotate(25deg) translate(18%,-2%);"
                                 src="${shs[id].photo}">
                        </div>
                    </div></a>
`;

        })
        const editss = document.querySelectorAll('.pencil');
        const elemetlar = document.querySelectorAll('.section_center_center_element');

        ekssssss.addEventListener('click', () => {
            madall.style.opacity = '0';
            madall.style.display = 'none';
        });

        editss.forEach((item, index) => {
            item.addEventListener('click', () => {
                madall.style.opacity = '1';
                madall.style.display = 'flex';
                ras.src = elemetlar[index].getAttribute('data-photo');
                ras.style.opacity = '1';
                inp.value = elemetlar[index].getAttribute('data-name');
                ids = elemetlar[index].getAttribute('data-id');
            });
        });
    })
    .catch(error => {
        console.error('Error fetching genres:', error);
    });
let ids = null
