new TypeIt('#typing', {
    strings: ['Take <span id="active">care</span>', 'of you finances'],
    speed: 40,
})
    .move(-16, {speed: 90,delay: 800})
    .delete(4, {delay: 800})
    .type('<span id="active">charge</span>', {delay: 2000})
    .delete(6, {delay: 1000})
    .type('<span id="active">control</span>', {delay: 1000})
    .go()


let pic = document.querySelector('.hero__img img')

pic.addEventListener('click', ()=> {
    let newAudio = document.createElement('Audio')
    newAudio.setAttribute('src', '/static/coin.mp3')
    // newAudio.setAttribute('preload', 'auto')
    newAudio.volume = 0.3
    console.log('playing audio')
    newAudio.play()
    // audio.play()
})
