<template>

<div class="word-cloud-card">
    <div class="word-cloud-title">Все слова</div>
    <canvas ref="allElement" width="800px" height="400px"></canvas>

    <div class="word-cloud-title">Существительные</div>
    <canvas ref="nounsElement" width="800px" height="400px"></canvas>

    <div class="word-cloud-title">Глаголы</div>
    <canvas ref="verbsElement" width="800px" height="400px"></canvas>

    <div class="word-cloud-title">Прилагалтельные</div>
    <canvas ref="adjectivesElement" width="800px" height="400px"></canvas>

    
</div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch} from 'vue';
import type { Ref } from 'vue'
import axios from 'axios';
import WordCloud from 'wordcloud';
import type { ListEntry } from 'wordcloud';

const tagTypes: (keyof WordFrequency)[] = [ 'all', 'verbs', 'adjectives', 'nouns'];

const allElement: Ref<null | HTMLElement> = ref(null);
const nounsElement: Ref<null | HTMLElement> = ref(null);
const adjectivesElement: Ref<null | HTMLElement> = ref(null);
const verbsElement: Ref<null | HTMLElement> = ref(null);

const props = defineProps<{
startYear: number,
endYear: number
}>()

watch(() => [props.startYear, props.endYear], async () => {
  await fetchWordFrequency()
  initWordCloud();
});

const elementAndType: [Ref<null | HTMLElement>, string][] = [
  [allElement, 'all'], 
  [verbsElement,'verbs'], 
  [adjectivesElement, 'adjectives'], 
  [nounsElement, 'nouns']
];

interface WordCloudHtmlElements{
  verbs: Ref<HTMLElement | null>;
  adjectives: Ref<HTMLElement| null>;
  nouns: Ref<HTMLElement | null>;
  all: Ref<HTMLElement | null>;
}

const wordCloudHtmlElements: WordCloudHtmlElements ={
  verbs: ref(null),
  adjectives: ref(null),
  nouns: ref(null),
  all: ref(null),
}

interface FreqDict{
  [key: string]: number;
}

interface WordFrequency{
  verbs: ListEntry[] | null;
  adjectives: ListEntry[] | null;
  nouns: ListEntry[] | null;
  all: ListEntry[] | null;
}


const wordFrequency: WordFrequency = reactive({
  verbs: null,
  adjectives: null,
  nouns: null,
  all: null
});

interface colorDict{
  [key: string]: string;
}

const wordColor: Ref<colorDict | null> = ref(null);

function transformFrequencyToTuple(freqDict: FreqDict): ListEntry[] {
  const arr = [];
  let freqTuple: ListEntry
  for (const [key, value] of Object.entries(freqDict)) {
    freqTuple = [key, value];
    arr.push(freqTuple);
  }
  return arr;
}


// Function to fetch word frequency
async function fetchWordFrequency() {

  for (const tagType of tagTypes) {
    let data: FreqDict
    try {
      const response = await axios.get<FreqDict>(`http://127.0.0.1:8000/app/word_cloud/word_frequency`, {
        params: { 
          tag_type: tagType
        }
      });
      data = response.data;
      let freqTuple: ListEntry[] = transformFrequencyToTuple(data)
      wordFrequency[tagType as keyof WordFrequency] = freqTuple;
    } catch (error) {
      if (axios.isAxiosError(error)){
        console.error(error);
      }
      else {
        throw error;
      }
    }
  }
}

// Function to fetch word color
async function fetchWordColor() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/app/word_cloud/word_color');
    wordColor.value = response.data;
  } catch (error) {
    console.error(error);
  }
}


function initWordCloud() {
  console.log(wordFrequency['all'])
  if (
    wordColor.value === null
  ){
    throw new Error('Word color is not initialized');
  }
  for (const [element, tagType] of elementAndType) {
    const wordList = wordFrequency[tagType as keyof WordFrequency]
    if (wordList === null){
      throw new Error('wordFrequency for tagType '+ tagType +' is null');
    }
    if (element.value === null) {
      throw new Error(`element for tagType ${tagType} is null`);
    }
    renderWordCloud(element.value, wordList);

  }
}


function renderWordCloud(element: HTMLElement, wordList: ListEntry[]){
  WordCloud(element,
      {
        list: wordList,
        color: (word) => wordColor.value![word],
        backgroundColor: '#2b2b2b',
        gridSize: 10,
        weightFactor: 1,
        fontFamily: "sans-serif",
        rotateRatio: 0.3,
        shuffle: false,
        rotationSteps: 2,
        shape: "circle",
        ellipticity: 0.6,
        shrinkToFit: true,
        minSize: 14,
        classes: 'word-cloud-item',
      }
    ) 
}



// onMounted lifecycle hook
onMounted(async () => {
  await fetchWordFrequency();
  await fetchWordColor();
  initWordCloud();
});
</script>


<style scoped>
body {
  font-family: sans-serif;
}

.text-center {
  text-align: center;
}

.word-cloud-container {
  display: flex;
}

.word-cloud-card {
  width: 100%;
}

.word-cloud-title {
  font-weight: bold;
  font-size: 1.2em;
  text-align: center;
  text-decoration: underline;
}

#word-cloud-canvas-hover-box {
  pointer-events: none;
  position: absolute;
  box-shadow: 0 0 200px 200px rgba(255, 255, 255, 0.5);
  border-radius: 50px;
  border-style: solid;
  cursor: pointer;
}

#word-cloud-html > span {
    transition: text-shadow 1s ease, opacity 1s ease;
    -webkit-transition: text-shadow 1s ease, opacity 1s ease;
    -ms-transition: text-shadow 1s ease, opacity 1s ease;
  }

 #word-cloud-html > span:hover {
    text-shadow: 0 0 10px, 0 0 10px #fff, 0 0 10px #fff, 0 0 10px #fff;
    opacity: 0.5;
  }
</style>