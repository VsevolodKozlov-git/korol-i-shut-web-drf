<template>
<div ref="cntPlotElement"></div>

</template>


<script setup lang="ts">
import { onMounted, ref, watch} from 'vue';
import type { Ref } from 'vue'
import axios from 'axios';
import Plotly from 'plotly.js-dist-min'
import type {Data, Layout} from 'plotly.js-dist-min';


const cntPlotElement: Ref<null | HTMLElement> = ref(null);

async function onUpdate(){
  await fetchSongsSentiment();
  await createSongCountPlot();
  // todo do async run for each plot
}

onMounted(async () => {
  onUpdate();
});

const props = defineProps<{
startYear: number,
endYear: number
}>()

watch(() => [props.startYear, props.endYear], async () => {
  onUpdate();
});

interface AlbumEntryFromGet{
  title: string
  year: number
}

interface SongEntryFromGet{
  title: string,
  album: AlbumEntryFromGet
  negative: number
  positive: number
  neutral: number
}


const fetchedSongsSentiment: Ref<SongEntryFromGet[] | null> = ref(null);


// Function to fetch word frequency
async function fetchSongsSentiment() {
  try {
      const response = await axios.get<SongEntryFromGet[]>(`http://127.0.0.1:8000/app/vizualization/sentiment`, {
        params: { 
          year_min: props.startYear,
          year_max: props.endYear
        }
      });
      fetchedSongsSentiment.value = response.data;

    } catch (error) {
      if (axios.isAxiosError(error)){
        console.error(error);
      }
      else {
        throw error;
      }
    }
}


class SentimentCnt{
    negative: number = 0 
    positive: number = 0
    neutral: number = 0
  }

async function createSongCountPlot(){
  if (cntPlotElement.value == null) {
    throw Error('cntPlotElement is not defined');
  }

  const sentimentCnt = countSongsSentiment() 
  const xvalues: string[] = ['Негативная', 'Нейтральная', 'Позитивная']
  const yvalues: number[] = [
    sentimentCnt.negative, 
    sentimentCnt.neutral, 
    sentimentCnt.positive
  ]

  var data: Data[] = [
    {
      x: xvalues,
      y: yvalues,
      type: 'bar'
    }
  ];
  const layout: Partial<Layout> = {
    xaxis: {
      title: 'Эмоциональная окраска',
    },
    yaxis: {
      title: 'Количество песен',
    }
  }
  await Plotly.newPlot(cntPlotElement.value, data, layout);
}


function countSongsSentiment(): SentimentCnt {
  if (fetchedSongsSentiment.value === null){
    throw new Error('fetchSongsSentiment() must be called before countSongsSentiment()');
  }

  const sentimentCnt = new SentimentCnt();
  for (const songSentiment of fetchedSongsSentiment.value) {
    const keys: (keyof SentimentCnt)[] = ['negative', 'neutral', 'positive']
    const vals = [songSentiment.negative, songSentiment.neutral, songSentiment.positive];
    const maxIndex = getArgMax(vals)
    sentimentCnt[keys[maxIndex]] += 1;
  }

  return sentimentCnt;
}
  

  


function getArgMax(array: any[]): number {
  return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1];
}





</script>