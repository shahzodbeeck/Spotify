let url = window.location.href;
let match = url.match(/\/playlist\/([^/]+)/);
let nextWord = match[1];


fetch(`/api_play/${nextWord}`)
    .then(response => response.json())
    .then(jsons => {
        let json = 0
        json = jsons.music
        console.log(json)

        function create(music) {
            const table = document.querySelector('.tbody')
            table.innerHTML = ``
            music.forEach((item, id) => {
                table.innerHTML += `<tr class="section_table_table_tr1" data-id='${music[id].number}' data-photo="${music[id].photo}" data-caption="${music[id].text}" data-name="${music[id].song}">
                        <td class="section_table_table_tr1_td1"><span class="opacity">${music[id].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i></td>
                        <td class="section_table_table_tr1_td2">
                            <ul class="section_table_table_tr1_td2_ul">
                                <li class="section_table_table_tr1_td2_ul_li"><img src="${music[id].photo}" style="width: 40px;height: 40px;object-fit: cover" alt=""></li>
                                <li class="section_table_table_tr1_td2_ul_li" style="width: 150px;height: 40px;">
                                    <div class="section_table_table_tr1_td2_ul_li_h1">${music[id].song}</div>
                                    <div class="section_table_table_tr1_td2_ul_li_h2">${music[id].artist}</div>
                                </li>
                            </ul>
                        </td>
                        <td class="section_table_table_tr1_td3">${music[id].album}</td>
                        <td class="section_table_table_tr1_td4">${music[id].data}</td>
                        <td class="section_table_table_tr1_td5">${music[id].duration}</td>
                    </tr>
`;
            })
        }

        create(json)

        let play_unplay = document.querySelector('.section_bottom_ul_li_dumaloq'), music = document.getElementById('1'),
            icon = document.querySelector('.played'),
            greens = document.querySelectorAll('.section_table_table_tr1_td2_ul_li_h1'),
            loads = document.querySelectorAll('.section_table_table_tr1_td1'),
            main_play = document.getElementById('main_play'),
            play_2 = document.querySelector('.footer_center_top_center_center'),
            nexts = document.querySelector('#next'), prevs = document.querySelector('#prev'),
            nik_mus = document.querySelector('.footer_left_right_top'),
            artist_mus = document.querySelector('.footer_left_right_bottom'), mud = document.querySelector('.mud'),
            progres = document.querySelector('.progress__filled'),
            times = document.querySelector('.footer_center_bottom_left'),
            progress2 = document.querySelector('.footer_center_bottom_center'),
            pauseee = document.querySelectorAll('.section_table_table_tr1_td1'),
            progres2 = document.querySelector('.progress__filled2'),
            progress22 = document.querySelector('.footer_right_last_right'),
            mute = document.querySelector('.footer_right_last_left'), good = document.querySelector('.mute'),
            ree = document.querySelector('.footer_center_rigth'), iconnn = document.querySelector('.reaap')
        let index = 0
        ree.addEventListener('click', () => {
            if (repla === 0) {
                iconnn.style.color = `#1ed760`
                repla = 1
            } else if (repla === 1) {
                iconnn.style.color = `#a7a7a7`
                repla = 0
            }
        })

        function play() {

            play_unplay.addEventListener('click', () => {
                if (music.paused) {
                    music.src = `${json[0].music}`
                    greens[index].classList.add('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div><i class="fa-solid fa-pause puq2"></i>`
                    music.play()
                    icon.classList.remove('fa-play')
                    icon.classList.add('fa-pause')
                    main_play.classList.remove('fa-play')
                    main_play.classList.add('fa-pause')
                    nik_mus.innerHTML = `${json[index].song}`
                    artist_mus.innerHTML = `${json[index].artist}`
                    mud.src = `${json[index].photo}`
                } else {
                    music.pause()
                    icon.classList.remove('fa-pause')
                    icon.classList.add('fa-play')
                    main_play.classList.remove('fa-pause')
                    main_play.classList.add('fa-play')
                    greens[index].classList.remove('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`

                }
            })
            play_2.addEventListener('click', () => {

                if (music.paused) {
                    music.src = `${json[0].music}`
                    greens[index].classList.add('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div><i class="fa-solid fa-pause puq2"></i>`

                    music.play()
                    icon.classList.remove('fa-play')
                    icon.classList.add('fa-pause')
                    main_play.classList.remove('fa-play')
                    main_play.classList.add('fa-pause')
                    nik_mus.innerHTML = `${json[index].song}`
                    artist_mus.innerHTML = `${json[index].artist}`
                    mud.src = `${json[index].photo}`
                } else {
                    music.pause()
                    icon.classList.remove('fa-pause')
                    icon.classList.add('fa-play')
                    main_play.classList.remove('fa-pause')
                    main_play.classList.add('fa-play')
                    greens[index].classList.remove('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`

                }
            })
        }

        play()

        nexts.addEventListener('click', () => {
            if (index >= json.length - 1) {
                icon.classList.remove('fa-pause')
                icon.classList.add('fa-play')
                greens[index].classList.remove('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`

                greens[0].classList.add('green')
                loads[0].innerHTML = ``
                loads[0].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                icon.classList.remove('fa-play')
                icon.classList.add('fa-pause')
                main_play.classList.remove('fa-play')
                main_play.classList.add('fa-pause')
                index = 0
            } else {
                icon.classList.remove('fa-pause')
                icon.classList.add('fa-play')
                greens[index].classList.remove('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`
                index++
                music.src = `${json[index].music}`
                greens[index].classList.add('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                icon.classList.remove('fa-play')
                icon.classList.add('fa-pause')
            }
            nik_mus.innerHTML = `${json[index].song}`
            artist_mus.innerHTML = `${json[index].artist}`
            mud.src = `${json[index].photo}`
            music.play()
        })
        prevs.addEventListener('click', () => {
            if (0 >= index) {
                icon.classList.remove('fa-pause')
                icon.classList.add('fa-play')
                greens[index].classList.remove('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`

                greens[json.length - 1].classList.add('green')
                loads[json.length - 1].innerHTML = ``
                loads[json.length - 1].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                icon.classList.remove('fa-play')
                icon.classList.add('fa-pause')
                main_play.classList.remove('fa-play')
                main_play.classList.add('fa-pause')
                index = json.length - 1
            } else {
                icon.classList.remove('fa-pause')
                icon.classList.add('fa-play')
                greens[index].classList.remove('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`
                index--
                music.src = `${json[index].music}`
                greens[index].classList.add('green')
                loads[index].innerHTML = ``
                loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                icon.classList.remove('fa-play')
                icon.classList.add('fa-pause')
            }
            nik_mus.innerHTML = `${json[index].song}`
            artist_mus.innerHTML = `${json[index].artist}`
            mud.src = `${json[index].photo}`
            music.play()
        })
        music.addEventListener("timeupdate", (e) => {
            const {currentTime, duration} = e.srcElement
            const minutes = Math.floor(music.currentTime / 60);
            const seconds = Math.floor(music.currentTime % 60);
            const minutesw = Math.floor(music.duration / 60);
            const secondsw = Math.floor(music.duration % 60);
            times.innerHTML = `${minutes} : ${seconds}`
            let foiz = (currentTime / duration) * 100;
            progres.style.flexBasis = `${foiz}%`
            document.querySelector('.footer_center_bottom_right').innerHTML = `${minutesw}:${secondsw}`
            if (repla === 0) {
                if (foiz === 100) {
                    if (index >= json.length - 1) {
                        icon.classList.remove('fa-pause')
                        icon.classList.add('fa-play')
                        greens[index].classList.remove('green')
                        loads[index].innerHTML = ``
                        loads[index].innerHTML = `${json[index].number}`

                        greens[0].classList.add('green')
                        loads[0].innerHTML = ``
                        loads[0].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                        icon.classList.remove('fa-play')
                        icon.classList.add('fa-pause')
                        main_play.classList.remove('fa-play')
                        main_play.classList.add('fa-pause')
                        index = 0
                    } else {
                        icon.classList.remove('fa-pause')
                        icon.classList.add('fa-play')
                        greens[index].classList.remove('green')
                        loads[index].innerHTML = ``
                        loads[index].innerHTML = `${json[index].number}`
                        index++
                        music.src = `${json[index].music}`
                        greens[index].classList.add('green')
                        loads[index].innerHTML = ``
                        loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                        icon.classList.remove('fa-play')
                        icon.classList.add('fa-pause')
                    }
                    nik_mus.innerHTML = `${json[index].song}`
                    artist_mus.innerHTML = `${json[index].artist}`
                    mud.src = `${json[index].photo}`
                    music.play()
                }
            } else if (repla === 1) {
                music.play()
            }
        })
        progress2.addEventListener("click", (event) => {
            let widht = progress2.clientWidth
            let clicked = event.offsetX
            let duration = music.duration

            let setProgress = (clicked / widht) * duration
            progres.style.flexBasis = `${setProgress}`
            music.currentTime = setProgress

        })
        pauseee.forEach((item, id) => {
            item.addEventListener('click', (e) => {
                if (index === id) {
                    if (music.paused) {
                        music.play()
                        greens[index].classList.add('green')
                        loads[index].innerHTML = ``
                        loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div><i class="fa-solid fa-pause puq2"></i>`
                        music.play()
                        icon.classList.remove('fa-play')
                        icon.classList.add('fa-pause')
                        main_play.classList.remove('fa-play')
                        main_play.classList.add('fa-pause')
                        nik_mus.innerHTML = `${json[index].song}`
                        artist_mus.innerHTML = `${json[index].artist}`
                        mud.src = `${json[index].photo}`
                    } else {
                        music.pause()
                        icon.classList.remove('fa-pause')
                        icon.classList.add('fa-play')
                        main_play.classList.remove('fa-pause')
                        main_play.classList.add('fa-play')
                        greens[index].classList.remove('green')
                        loads[index].innerHTML = ``
                        loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`
                    }
                } else {
                    icon.classList.remove('fa-pause')
                    icon.classList.add('fa-play')
                    greens[index].classList.remove('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `<span class="opacity">${json[index].number}</span><i
                                class="fa-solid fa-play puq" style="color: #FFFFFF"></i>`
                    index = id
                    music.src = `${json[index].music}`
                    music.play()
                    greens[index].classList.add('green')
                    loads[index].innerHTML = ``
                    loads[index].innerHTML = `        <div class="loading">
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                                <div class="load"></div>
                            </div>
<i class="fa-solid fa-pause puq2"></i>`
                    icon.classList.remove('fa-play')
                    icon.classList.add('fa-pause')
                    nik_mus.innerHTML = `${json[index].song}`
                    artist_mus.innerHTML = `${json[index].artist}`
                    mud.src = `${json[index].photo}`
                }
            })
        })
        progress22.addEventListener("click", (event) => {
            let widht = progress22.clientWidth
            let clicked = event.offsetX
            let sound = music.volume
            let setProgress = (clicked / widht) * sound
            music.volume = setProgress / sound
            console.log(sound)
            progres2.style.flexBasis = `${clicked}%`
        })
        progress22.addEventListener('wheel', (event) => {
            let widht = progress22.clientWidth
            let clicked = progres2.clientWidth
            if (event.deltaY < 0) {
                clicked += 0.0005
                let sound = music.volume
                let setProgress = (clicked / widht) * sound
                music.volume = setProgress / sound
                progres2.style.flexBasis = `${clicked}%`
            } else if (event.deltaY > 0) {
                let widht = progress22.clientWidth
                clicked -= 0.005
                let sound = music.volume
                let setProgress = (clicked / widht) * sound
                music.volume = setProgress / sound

                progres2.style.flexBasis = `${-clicked}%`
            }
        });
        mute.addEventListener('click', () => {
            if (music.volume === 0) {
                music.volume = 1
                progres2.style.flexBasis = `${100}%`
                good.classList.remove('fa-volume-off')
                good.classList.add('fa-volume-high')
            } else if (music.volume > 0) {
                good.classList.remove('fa-volume-high')
                good.classList.add('fa-volume-off')
                music.volume = 0
                progres2.style.flexBasis = `${0}%`
            }
        })
        document.querySelectorAll('.section_table_table_tr1').forEach((item, id) => {
            item.addEventListener("contextmenu", function (event) {
                event.preventDefault();
                document.querySelector('.modal_for_edit1').style.display = `flex`
                document.querySelector('.aaaaaawefwefwa').href = `http://127.0.0.1:5000/del_play/${document.querySelectorAll('.section_table_table_tr1')[id].getAttribute('data-id')}/${nextWord}`
            })
        });
        document.querySelector('nav').addEventListener('click', () => {
            document.querySelector('.modal_for_edit1').style.display = `none`
        })

        document.querySelector('.section_center_right_center').innerHTML = `${jsons.album.name}`
        document.querySelector('.section_center_right_bottom_top').innerHTML = `${jsons.album.caption}`
        document.querySelector('.hehehehe').innerHTML = `${jsons.album.songs} songs`
        document.querySelector('.section_center_left_photo').style.backgroundImage = `url(${jsons.album.photo})`
        document.querySelector('.section_center_left_photo').style.backgroundSize = `cover`
        document.querySelector('.section_center').style.background = `rgba(${jsons.album.rgba})`
        document.querySelector('.section_top').style.background = `rgba(${jsons.album.rgba})`
    })
    .catch(error => {
        console.error('Error fetching genres:', error);
    });
document.querySelector('.searches').addEventListener('change', () => {
    let qiymat = document.querySelector('.searches').value
    console.log(qiymat)
    const formData = new FormData();
    formData.append('text', qiymat);
    fetch('/search_music', {
        method: 'POST', body: formData,
    })
        .then(response => response.json())
        .then(jsons => {
            json = jsons

            function create(musics) {
                const table = document.querySelector('.section_search_bottom')
                table.innerHTML = ``
                musics.forEach((item, id) => {
                    table.innerHTML += `   <div class="music"
                             style="width: 100%; height: 66px; border-radius: 5px; display: flex; align-items: center;">
                            <div class="music_left"
                                 style="background: url(${musics[id].photo}); background-size: cover; height: 40px;width: 40px;">

                            </div>
                            <div class="music_center"
                                 style="width: 150px; display: flex;flex-direction: column; align-items: flex-start;justify-content: space-around;">
                                <div class="music_center_top" style="margin-left: 4px; color: white; font-size: 13px">
                                   ${musics[id].name}
                                </div>
                                <div class="music_center_bottom" style="margin-left: 4px; color: white; font-size: 14px"   >
                                   ${musics[id].user}
                                </div>
                            </div>
                            <div class="music_right"
                                 style="width: 990px;height: 64px; display: flex;align-items: center;justify-content: flex-end;">
                                <h3 data-id="${musics[id].id}" class="add_mandat" style="width: 70px;height: 30px;border-radius: 15px;background: transparent; color: white; border: 0.5px solid white; display: flex; justify-content: center; align-items: center;">
                                    Add</h3>
                            </div>
                        </div>`;
                })
            }

            create(json)

            document.querySelectorAll('.add_mandat').forEach((item, id) => {
                item.addEventListener('click', () => {
                    console.log('ishladi')
                    let dasda = document.querySelectorAll('add_mandat')
                    fetch(`/add_play/${item.getAttribute('data-id')}/${nextWord}`)
                        .then(response => response.json())
                        .then(jsons => {
                            location.reload();
                        })
                        .catch(error => {
                            console.error('Error fetching genres:', error);
                        });
                })
            })
        })
        .catch(error => {
            console.error('Error fetching genres:', error);
        });
})