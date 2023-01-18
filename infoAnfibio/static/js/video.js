
document.addEventListener("DOMContentLoaded",()=>{
  video = document.getElementById('vVid')
  vPlay = document.getElementById("vPlay")
  vPlayIco = document.getElementById("vPlayIco")
  vNow = document.getElementById("vNow")
  vTime = document.getElementById("vTime")
  vSeek = document.getElementById("vSeek")
  vVolume = document.getElementById("vVolume")
  vVolIco = document.getElementById("vVolIco")

  vidStart = true

  video.addEventListener("canplay", () => { if (vidStart) {
    vidStart = false;
  }});

  video.addEventListener("play", () => {
    vPlayIco.innerHTML = "pause";
  });

  video.addEventListener("pause", () => {
    vPlayIco.innerHTML = "play_arrow";
  });

  vPlay.addEventListener("click", () => {
    if (video.paused) { video.play(); }
    else { video.pause(); }
  });

  vVolume.addEventListener("change", () => {
    video.volume = vVolume.value;
    vVolIco.innerHTML = (vVolume.value==0 ? "volume_mute" : "volume_up");
  });

  video.addEventListener("canplay", () => {
    vPlay.disabled = false;
    vVolume.disabled = false;
    vSeek.disabled = false;
  });

  video.addEventListener("waiting", () => {
    vPlay.disabled = true;
    vVolume.disabled = true;
    vSeek.disabled = true;
  });

  video.addEventListener("loadedmetadata", () => {
    vNow.innerHTML = timeString(0);
    vTime.innerHTML = timeString(video.duration);
  });

  video.addEventListener("timeupdate", () => {
    vNow.innerHTML = timeString(video.currentTime);
  });

  video.addEventListener("loadedmetadata", () => {
    vSeek.max = Math.floor(video.duration);
    var vSeeking = false;

    vSeek.addEventListener("input", () => {
      vSeeking = true;
    });

    vSeek.addEventListener("change", () => {
      video.currentTime = vSeek.value;
      if (!video.paused) { video.play(); }
      vSeeking = false;
    });

    video.addEventListener("timeupdate", () => {
      if (!vSeeking) { vSeek.value = Math.floor(video.currentTime); }
    });
  });

  var timeString = (secs) => {
    let ss = Math.floor(secs)
    let hh = Math.floor(ss / 3600)
    let mm = Math.floor((ss - (hh * 3600)) / 60)
    ss = ss - (hh * 3600) - (mm * 60)

    if (hh>0) { mm = mm<10 ? "0"+mm : mm; }
    ss = ss<10 ? "0"+ss : ss;
    return hh>0 ? `${hh}:${mm}:${ss}` : `${mm}:${ss}`
  };

})