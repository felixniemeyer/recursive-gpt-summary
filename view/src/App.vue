<script setup lang="ts">
import axios from 'axios'
import TitleColumn from './components/TitleColumn.vue'

const base = import.meta.env.BASE_URL

axios.interceptors.request.use((config: any) => {
  config.headers['cache-control'] = 'max-age=2147483647'; // always use cache, content never changes 
  config.url = base + config.url
  return config;
});

// parse charIndex (behind #)
const charIndex = window.location.hash.slice(1)

async function init() {
  // load levels
  const levels = await axios.get('/volume/levels', {responseType: 'text'})

  // setup columns

  // title column

  // text columns

  // svg column
}

</script>

<template>
  <div id=container>
    <div class="column arrow">▶</div>
    <TitleColumn />
    <TitleColumn />
    <TitleColumn />
    <TitleColumn />
    <div class="column arrow">◀</div>
  </div>
  <div id=top-fadein></div>
  <div id=bottom-fadein></div>
</template>

<style scoped>
#container {
  display: flex;
  overflow-x: scroll;
  height: 100vh;
}

#top-fadein, #bottom-fadein {
  position: fixed; 
  left: 0; 
  height: 2rem; 
  width: 100vw; 
}

#top-fadein {
  top: 0; 
  background: linear-gradient(to bottom, #ffff 20%, #fff0);
}
  
#bottom-fadein {
  bottom: 0; 
  background: linear-gradient(to bottom, #fff0, #ffff 80%);
}

.column {
  flex: 0 0 auto; /* set flex-grow, flex-shrink and flex-basis to 0, so the boxes don't stretch */
  margin-right: 10px; /* add margin between the boxes */
  height: 100%;
  box-sizing: border-box;
  padding: 1rem; 
  overflow-y: scroll;
  align-items: center;
}

.arrow {
  font-size: 3rem;
  line-height: 100vh;
  overflow-y: hidden;
  color: #888; 
  padding: 2rem; 
  user-select: none;
}

</style>
