<script setup lang="ts">
// vue router
import { RouterLink } from 'vue-router'
import * as config from '../config'

</script>

<template>
  <div>
    <h2> 
      Hallo!
    </h2>
    <p>Dies ist mein Tagebuch von etwa 2016 bis 2023.</p>
    <p>
      Ich habe damit begonnen, nur für mich selbst zu schreiben und es zur Bewältigung von Problemen
      zu verwenden, die ich im Leben und in meinem Geist habe. Es gibt wahrscheinlich auch eine Menge
      beängstigender Gedanken darin. Außerdem habe ich die Namen beibehalten und selbst für meine
      liebsten Freunde habe ich manchmal böse Gedanken gehabt, und ich hoffe, ihr könnt mir vergeben,
      dass ich sie hatte. Wenn ihr unsicher seid, sprecht mit mir, lasst uns das klären. Mein ganzes
      Leben lang habe ich Dinge für mich behalten und lange darüber nachgedacht. Ich öffne mich in
      diesen Tagen und verbinde mein Gehirn mit meinen Kollegen, ohne mich noch Sorgen zu machen,
      besser als ihr zu sein.
    </p>
    <p>
      Ich habe ein kleines Tool geschrieben, das ChatGPT als Grundlage verwendet, um den gesamten
      Inhalt meines Lebens rekursiv auf einige Absätze zusammenzufassen. Ich hoffe das es so leicht
      ist die Themen, die euch interessieren zu erkunden: durch alle Komprimierungsebenen hindurch bis
      hin zu den originalen Tagebucheinträgen.
    </p>
    <p>
      Ihr können dieses Tool und auch diese Web-Benutzeroberfläche selbst verwenden, es ist Open
      Source:<br/>
      <a href="https://github.com/felixniemeyer/recursive-gpt-summary" target="_blank">
        Recursive GPT Summary auf Github
      </a>
    </p>
    <p>Ich freue mich, alle Gedanken preiszugeben, die ich in der Vergangenheit hatte.</p>
    <RouterLink :to="config.rootFileId">Beginne zu lesen</RouterLink>
  </div>

  <div>
    <h2>
      <p>Hi there,</p>
    </h2>
    <p>this my diary from around 2016 until 2023.</p>
    <p>
      I started writing this only for myself and used it for dealing with problems that I have in
      life and in my mind. There is probably a bunch of scary thoughts in there as well. Also, I
      kept the names intact and even for my dearest friends I might sometimes have thought nasty
      thoughts and I hope you can forgive me for having them. If in doubt, talk to me, lets clarify.
      All my life, I have kept things to myself and thought about them in length. I am opening up
      these days and connecting my brain with my peers, not worried anymore about being better than
      you.
    </p>
    <p>
      I've written a small tool that is using chatGPT under the hood to summarize all the content of
      my life recursively down to a few paragraphs. I hope this makes it interesting to explore the
      topics that you are interested: through all levels of compression unto the original diary
      entries.
    </p>
    <p>
    You can use this tool and also this Web UI yourself, it's open source:<br/>
      <a href="https://github.com/felixniemeyer/recursive-gpt-summary" target="_blank">
        Recursive GPT Summary on Github</a
      >
    </p>
    <p>I'm happy to disclose all the thought's I had in the past.</p>
    <RouterLink :to="config.rootFileId">Start Exploring</RouterLink>
  </div>

</template>

<style scoped>
button {
  padding: 0.5rem; 
  margin: 0.5rem 0 ; 
}
h2 {
  margin-top: 2rem; 
}
p {
  margin: 0.5rem 0; 
}
</style>
