<template>
  <div class="album-box">
    <div class="album-art">
      <RecordIcon />
    </div>
    <div class="album-info">
      <span class="d-block">{{ title }}</span>
      <a class="d-block" href="#">{{ artist }}</a>
    </div>
    <div class="album-controls">
      <span class="clickable" @click="getSongs(id)">
        <PlayButton v-if="musicStore.currentAlbum !== id || !musicStore.isPlaying &&  musicStore.currentAlbum === id"/>
        <PauseButton v-if="musicStore.isPlaying && musicStore.currentAlbum === id" />
      </span>
    </div>
  </div>
</template>
<script setup>
import useMusicStore from '~/stores/useMusicStore';

const props = defineProps({
  id: Number,
  title: String,
  artist: String,
  artistId: Number  
});


const { id, title, artist, artistId } = props;

const musicStore = useMusicStore();

async function getSongs(id) {
    if (musicStore.currentAlbum !== id) {
      musicStore.updateCurrentAlbum(id)
      const response = await fetch(`/api/albums/${id}/songs`);
      const data = await response.json();
      musicStore.updateSong(data);
      musicStore.updatePlaying(true);
    } else {
      musicStore.updatePlaying(!musicStore.isPlaying);
    }
}

onUpdated(() => {
  console.log(musicStore.isPlaying)
})

</script>
<style lang="scss">
.album-box {
  border: 1px solid #eee;
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 3px;
  --shadow-color: 0deg 0% 54%;
  --shadow-elevation-low:
    0.3px 0.5px 0.7px hsl(var(--shadow-color) / 0.24),
    0.4px 0.8px 1px -1.2px hsl(var(--shadow-color) / 0.24),
    0.9px 1.7px 2.2px -2.5px hsl(var(--shadow-color) / 0.24);
    box-shadow: var(--shadow-elevation-low);
}

.album-controls {
  background: red;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  position: absolute;
  right: 5px;
  bottom: 22%;
  --shadow-color: 286deg 36% 56%;
  --shadow-elevation-medium:
    0.3px 0.5px 0.7px hsl(var(--shadow-color) / 0.36),
    0.8px 1.6px 2px -0.8px hsl(var(--shadow-color) / 0.36),
    2.1px 4.1px 5.2px -1.7px hsl(var(--shadow-color) / 0.36),
    5px 10px 12.6px -2.5px hsl(var(--shadow-color) / 0.36);
    box-shadow: var(--shadow-elevation-medium);
  span {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-40%);
  }
}

.album-art {
  background: grey;
  height: 200px;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  display: flex;
  justify-content: center;
  align-items: center;
  @media (min-width: 1920px) {
    height: 250px;
  }
}

.album-info {
  padding: 27px 20px;
}
</style>