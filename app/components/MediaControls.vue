<template>
  <footer>
    <div class="audio-controls-grid">
      <div></div>
      <div class="audio-controls">
        <audio preload="metadata" id="player" @timeupdate="getCurrentTime" controls style="display: none;">
          <source :src="music" type="audio/ogg">
          Your browser does not support the audio element.
        </audio>
        <div>
          <span class="clickable">
            <BackwardStep />
          </span>
          <span class="clickable">
            <PlayButton v-if="!isPlaying" @click="play" />
            <PauseButton v-if="isPlaying" @click="play" />
          </span>
          <span class="clickable">
            <ForwardStep />
          </span>
        </div>
        <div>
          <progress min="0" max="100" :value="progress" />
        </div>
        <div>
          <span>{{ time(currentSeek) }}</span>
          /
          <span>{{ time(songDuration) }}</span>
        </div>
      </div>


    </div>
  </footer>
</template>
<script setup>
import BackwardStep from '~/components/BackwardStep.vue';
import ForwardStep from '~/components/ForwardStep.vue';
import PlayButton from '~/components/PlayButton.vue';

const progress = ref(0);
const currentSeek = ref(0);
const songDuration = ref(0);
const isPlaying = ref(false);

const music = '/api/songs/2/blob'

function getCurrentTime(event) {
  const controls = event.target
  songDuration.value = controls.duration;
  currentSeek.value = controls.currentTime;
  progress.value = (controls.currentTime / controls.duration) * 100;
}
const zeroPad = (num, places) => String(num).padStart(places, '0');

function play() {
  if (!isPlaying.value) {
    document.querySelector("#player").play()
  } else {
    document.querySelector("#player").pause()
  }

  isPlaying.value = !isPlaying.value;
}

function time(totalSeconds) {
  if (totalSeconds) {
    const minutes = Math.floor(~~(totalSeconds / 60)) || 0;
    const seconds = totalSeconds % 60;

    return `${minutes}:${zeroPad(Math.round(seconds), 2)}`;
  } else {
    return "0:00";
  }

}

onMounted(() => {
})

</script>
<style lang="scss">
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

.audio-controls {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}
</style>