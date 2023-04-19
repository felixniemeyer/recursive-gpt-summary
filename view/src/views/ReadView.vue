<script setup lang=ts>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import axios from 'axios'

const base = import.meta.env.BASE_URL

axios.interceptors.request.use((config: any) => {
  config.headers['cache-control'] = 'max-age=2147483647'; // always use cache, content never changes 
  config.url = base + config.url
  return config;
});

const route = useRoute()
const router = useRouter()

async function loadOrigins() {
  const response = await axios.get('/volume/origins.json')
  return response.data
}
const originsPromise = loadOrigins()

async function loadSummaries() {
  const response = await axios.get('/volume/summaries.json')
  return response.data
}
const summariesPromise = loadSummaries()

const summaryText = ref(undefined as string | undefined)
const originTexts = ref([] as string[])
const originFiles = ref([] as string[])

const previousId = ref(undefined as string | undefined)
const nextId = ref(undefined as string | undefined)

const summaryFile = ref(undefined as string | undefined)

const originClickable = ref(false)

let level = route.params.level
let id = route.params.id

async function loadData() {
  console.log('loading data') 
  level = route.params.level
  id = route.params.id
  // get plain text file
  axios.get(`/volume/${level}/${id}`, {responseType: 'text'}).then((response) => {
    summaryText.value = response.data.trim()
  })

  // check whether we can go back and forth
  previousId.value = undefined
  nextId.value = undefined
  if (typeof id === 'string') {
    let idInt = parseInt(id)
    console.log(idInt)
    if (idInt > 0) {
      previousId.value = ('0000' + (idInt - 1)).slice(-5)
    }       // check if file for next id does exists
    // pad with zeros 5 digits without padStart
    const potentialNextId = ('0000' + (idInt + 1)).slice(-5)

    axios.head(`/volume/${level}/${potentialNextId}`).then((response) => {
      if(response.status === 200) {
        nextId.value = potentialNextId
      }
    }).catch(() => {
      console.log('the above failed axios request is ok')
    })
  } 

  originsPromise.then((origins) => {
    originTexts.value = []
    originFiles.value = origins[level + '/' + id]
    originFiles.value.forEach((origin: string) => {
      axios.get(`/volume/${origin}`, {responseType: 'text'}).then((response) => {
        originTexts.value.push(response.data.trim())
      })
    })
  })

  summariesPromise.then((summaries) => {
    const r = summaries[level + '/' + id]
    if (r !== undefined && r.length > 0) {
      summaryFile.value = r[0]
    } else {
      summaryFile.value = undefined
    }
  })

  originClickable.value = typeof level === 'string' && parseInt(level) > 1
}

async function navigate(file: string) {
  // only if no text was selected
  if (window.getSelection()?.toString() === '') {
    router.push('/read/' + file)
  }
}

router.afterEach(loadData)

loadData()


</script>

<template>
  <div class=left>
    <h2> summary </h2>
    <p class=info>
      level {{ level }}
    </p>
    <a class=button v-if="previousId != undefined"
                    :href="`${base}read/${level}/${previousId}`">
      <span>&#x25B2; </span></a>
    <p class=info>
      file {{ id }}
    </p>
    <pre
      :class="{clickable: summaryFile !== undefined}"
      @click="summaryFile !== undefined && navigate(summaryFile)"
    >{{ summaryText }}</pre> 
    <a class=button v-if="nextId != undefined"
                    :href="`${base}read/${level}/${nextId}`">
      <span>&#x25BC;</span></a>
  </div><div class=right>
    <h2> {{ originClickable ? 'summarized' : 'original' }} texts </h2>
    <p v-if=originClickable class=info>
      click any text to see the texts it summarizes
    </p>
    <p v-else class=info>
      you are looking at the original texts
    </p>
    <pre v-for="text, i in originTexts" :key="i"
         :class="{clickable: originClickable}"
         @click="originClickable && navigate(originFiles[i])">{{ text }}</pre>
  </div></template>
<style scoped>
.left, .right {
  display: inline-block;
  vertical-align: top; 
  padding: 1rem; 
  width: 50%;
  height: 100vh; 
  overflow-y: scroll;
}
h2 {
  text-align: center;
  margin-bottom: 0.5rem; 
}
.button {
  display: block;
  margin: 0 auto;
  padding: 0.5rem; 
  text-align: center;
  cursor: pointer !important;
}
.button span {
  font-size: 3rem; 
}
pre {
  margin: 1rem 0;
  padding: 0.5rem; 
  border-radius: 0.2rem;
  background-color: #8883;
  white-space: pre-wrap;       /* Since CSS 2.1 */
}
pre.clickable {
  cursor: pointer;
}
.info {
  font-size: 0.8rem;
  text-align: center;
}
</style>
