function play2() {
    var player = videojs('video');
    var sub = document.getElementById('sub');
    sub.innerHTML = "I am goooooooooood!!!!!";
    player.on('timeupdate', function (e) {
        if (player.currentTime() >= 3) {
            sub.innerHTML = "I am goooooooooood!!!!!2";
            player.pause();
        }
    });
    player.play();
}
function play() {
    document.getElementById('sub').innerHTML = 'test'
}