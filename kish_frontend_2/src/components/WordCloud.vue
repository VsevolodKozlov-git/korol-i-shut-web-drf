<template>

<div class="font-size" v-if="referenceWords">
  <table>
    <tr>
      <th>Слово</th>
      <th>Количество</th>
    </tr>
    <tr v-for="refrenceWord, index in referenceWords" :key="index">
      <td :style="{
      color: refrenceWord.color,
      fontSize: refrenceWord.fontSize+'pt',
      lineHeight: refrenceWord.fontSize +'pt'
      }">
        {{refrenceWord.word}}
      </td>
      <td>{{refrenceWord.count}}</td>
    </tr>
  </table>
</div>

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

interface ReferenceWord{
  word: string;
  color: string;
  fontSize: number;
  count: number;
}

let referenceWords: Ref<ReferenceWord[] | null> = ref(null);

const props = defineProps<{
startYear: number,
endYear: number
}>()

watch(() => [props.startYear, props.endYear], async () => {
  await fetchWordFrequency()
  initWordCloud();
  initReferenceWords();
});

const elementAndType: [Ref<null | HTMLElement>, keyof WordFrequency][] = [
  [allElement, 'all'], 
  [verbsElement,'verbs'], 
  [adjectivesElement, 'adjectives'], 
  [nounsElement, 'nouns']
];


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
          tag_type: tagType,  
          year_min: props.startYear,
          year_max: props.endYear
        }
      });
      data = response.data;
      let freqTuple: ListEntry[] = transformFrequencyToTuple(data)
      console.log(freqTuple);
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


function initReferenceWords(): void {
  const arr: ReferenceWord[] = [];
  if (wordFrequency.all === null) {
    throw new Error('Word frequency is null inside initReferenceWords ');
  }

  const maxFrequency = getMaxFrequency()
  const weightFactor = getWeightFactor(maxFrequency)
  const maxFont = Math.floor(maxFrequency * weightFactor)


  let neededFontSize = [
    maxFont,
    Math.floor(maxFont / 2),
    Math.floor(maxFont / 4),
    Math.floor(maxFont / 8)
  ]

  let neededFontSizeindex = 0;

  // сортируем по убыванию
  wordFrequency['all'].sort((a, b) => b[1] - a[1]);
  for (const [word, frequency] of wordFrequency['all']) {
    if (neededFontSizeindex > neededFontSize.length - 1) 
      break
  
    let fontSize = Math.floor(frequency * weightFactor)
    if (fontSize <= neededFontSize[neededFontSizeindex]) {
      neededFontSizeindex += 1;
      arr.push({
        word: word,
        color: wordColor.value![word],
        fontSize: fontSize,
        count: frequency
      })
    }
  }
  referenceWords.value = arr;
}

function initWordCloud() { 
  const tagTypeMinFontSize = {
    all: 14,
    nouns: 12,
    verbs: 12,
    adjectives: 8
  }
  if (wordColor.value === null)
    throw new Error('Word color is not initialized');

  let maxFrequency = getMaxFrequency();
  let weightFactor = getWeightFactor(maxFrequency);

  for (let [element, tagType] of elementAndType) {
    let wordList = wordFrequency[tagType]
    if (wordList === null){
      throw new Error('wordFrequency for tagType '+ tagType +' is null');
    }
    if (element.value === null) {
      throw new Error(`element for tagType ${tagType} is null`);
    }
    let minFontSize = tagTypeMinFontSize[tagType];

    WordCloud(element.value,
      {
        list: wordList,
        color: (word) => wordColor.value![word],
        backgroundColor: '#2b2b2b',
        gridSize: 5,
        weightFactor: weightFactor,
        fontFamily: "sans-serif",
        rotateRatio: 0.3,
        shuffle: false,
        rotationSteps: 2,
        shape: "circle",
        ellipticity: 0.6,
        shrinkToFit: true,
        minSize: minFontSize,
        classes: 'word-cloud-item',
      }
    ) 
  }
}

function getMaxFrequency(): number {
  const frequencys = wordFrequency['all']!.map((listEntry) => listEntry[1]);
  const maxFrequency = Math.max(...frequencys);
  return maxFrequency;
}

function getWeightFactor(maxFrequency: number): number {
  const BaseFactor = 121 / 1.3 
  return BaseFactor / maxFrequency;
}






// onMounted lifecycle hook
onMounted(async () => {
  await fetchWordFrequency();
  await fetchWordColor();
  initWordCloud();
  initReferenceWords();
});
</script>


<style scoped>
body {
  font-family: sans-serif;
}

.font-size{
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