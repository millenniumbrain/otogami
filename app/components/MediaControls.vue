<template>
  <footer>
    <div class="audio-controls-grid">
      <div></div>
      <div class="audio-controls">
        <audio autoplay="false" v-if="musicStore.songs.length > 0" id="player" @timeupdate="getCurrentTime" controls
          style="display: none;">
          <source :src="`/api/songs/${musicStore.songs[musicStore.currentTrack].songId}/blob`" type="audio/ogg">
          Your browser does not support the audio element.
        </audio>
        <div>
          <span class="clickable media-controls-seek-prev" @click="seekPrev()">
            <BackwardStep />
          </span>
          <span class="clickable media-controls-play-toggle">
            <PlayButton v-if="!musicStore.isPlaying" @click="playToggle" />
            <PauseButton v-if="musicStore.isPlaying" @click="playToggle" />
          </span>
          <span class="clickable media-controls-seek-next" @click="seekNext()">
            <ForwardStep />
          </span>
        </div>
        <div>
          <progress id="progress" min="0" max="100" :value="progress" />
        </div>
        <div>
          <span>{{ time(currentSeek) }}</span>
          /
          <span>{{ time(songDuration) }}</span>
        </div>
      </div>
      <div></div>

    </div>
  </footer>
</template>
<script setup>
import BackwardStep from '~/components/BackwardStep.vue';
import ForwardStep from '~/components/ForwardStep.vue';
import PlayButton from '~/components/PlayButton.vue';

import useMusicStore from '~/stores/useMusicStore';

const musicStore = useMusicStore();

const progress = ref(0);
const currentSeek = ref(0);
const songDuration = ref(0);

function getCurrentTime(event) {
  const controls = event.target
  songDuration.value = controls.duration;
  currentSeek.value = controls.currentTime;
  progress.value = (controls.currentTime / controls.duration) * 100;
}
const zeroPad = (num, places) => String(num).padStart(places, '0');

function playToggle() {
  const player = document.querySelector("#player");
  player.volume = 0.1;
  if (musicStore.isPlaying) {
    player.play()
  } else {
    player.pause()
  }

  const playing = !musicStore.isPlaying
  musicStore.updatePlaying(playing);
}

function seekNext() {
  const player = document.getElementById("player");
  if (player) {
    if (musicStore.currentTrack + 1 < musicStore.songs.length) {
      const track = musicStore.currentTrack + 1
      musicStore.updateCurrentTrack(track);
      player.stop();
      musicStore.updatePlaying(false);
      musicStore.updatePlaying(true)
    } else {
      musicStore.updateCurrentTrack(0)
    }
  }
}

watch(
  ()=> musicStore.currentAlbum,
  () => {
    const player = document.querySelector("#player");
    if (player) {
      player.stop();
      musicStore.updatePlaying(false);
    }
  }
)
function time(totalSeconds) {
  if (totalSeconds) {
    const minutes = Math.floor(~~(totalSeconds / 60)) || 0;
    const seconds = totalSeconds % 60;

    return `${minutes}:${zeroPad(Math.round(seconds), 2)}`;
  } else {
    return "0:00";
  }

}

watch(
  () => musicStore.isPlaying,
  () => {
    if (document) {
      const player = document.querySelector('#player');
      if (player) {
        player.volume = 0.1;
        if (musicStore.isPlaying) {
          player.play();
        } else {
          player.pause();
        }
      }

    }
  }
)

</script>
<style lang="scss">
footer {
  border-top: 1px solid #eee;
  position: fixed;
  bottom: 0;
  width: 100%;
}

.audio-controls-grid {
  width: 100%;
  height: 80px;
  border-top: black;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

.media-controls-play-toggle {
  background: red;
  width: 40px;
  height: 40px;
  position: relative;
  border-radius: 50%;
  --shadow-color: 286deg 36% 56%;
  --shadow-elevation-medium:
    0.3px 0.5px 0.7px hsl(var(--shadow-color) / 0.36),
    0.8px 1.6px 2px -0.8px hsl(var(--shadow-color) / 0.36),
    2.1px 4.1px 5.2px -1.7px hsl(var(--shadow-color) / 0.36),
    5px 10px 12.6px -2.5px hsl(var(--shadow-color) / 0.36);
  box-shadow: var(--shadow-elevation-medium);

  svg {
    top: 50%;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
    position: absolute;
  }
}

.media-controls-seek-prev, .media-controls-seek-next {
  position: relative;
  width: 40px;
  height: 40px;
  svg {
    top: 50%;
    left: 50%;
    transform: translateY(-50%) translateX(-50%);
    position: absolute;
  }
}

#progress {
  height: 12px;
  width: 100%;
  border: none;
  border-radius: 8px;
  background: #eee;

  &::-webkit-progress-value,
  &::-moz-progress-bar {
    background: red;
  }
}

.audio-controls {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;

  div {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>