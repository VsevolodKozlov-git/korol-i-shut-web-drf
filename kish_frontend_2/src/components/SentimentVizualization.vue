<template>
<div ref="cntPlotElement"></div>
<div ref="probabilitiesPlotElement"></div>

</template>


<script setup lang="ts">
import { onMounted, ref, watch} from 'vue';
import type { Ref } from 'vue'
import axios from 'axios';
import Plotly from 'plotly.js-dist-min'
import type {Data, Layout} from 'plotly.js-dist-min';


const cntPlotElement: Ref<null | HTMLElement> = ref(null);
const probabilitiesPlotElement: Ref<null | HTMLElement> = ref(null)


async function onUpdate(){
  await fetchSongsSentiment();
  createSongCountPlot();
  createProbabilitiesPlot();
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

function createSongCountPlot(){
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
      type: 'bar',
      marker: {
        color: ['#D63E3E', "#398CBD", "#8CC234"]
      }
    }
  ];
  const layout: Partial<Layout> = {
    xaxis: {
      title: 'Эмоциональная окраска',
    },
    yaxis: {
      title: 'Количество песен',
    },
    title: 'Распределение песен по эмоциональной окраске'
    
  }
  Plotly.newPlot(cntPlotElement.value, data, layout);
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


function createProbabilitiesPlot() {
  if (fetchedSongsSentiment.value === null){
    throw new Error('fetchedSongsSentiment.value is null. fetchSongsSentiment() must be called before createProbabilitiesPlot')
  }

  if (probabilitiesPlotElement.value === null) {
    throw Error('probabilitiesPlotElement is null');
  }
  const negativeProbabilities = getSentimentList('negative');
  const neutralProbabilities = getSentimentList('neutral');
  const positiveProbabilities = getSentimentList('positive');

  const data: Data[] = [
    {
      x: negativeProbabilities,
      type: 'histogram',
      name: 'Negative',
      xaxis: 'x1',
      yaxis: 'y',
      marker: {
        color: '#D63E3E',
      },
      xbins: {
        size: 0.05
      }
    },
    {
      x: neutralProbabilities,
      type: 'histogram',
      name: 'Neutral',
      xaxis: 'x2',
      yaxis: 'y',
      marker: {
        color: "#398CBD"
      },
      xbins: {
        size: 0.05
      }
    },
    {
      x: positiveProbabilities,
      type: 'histogram',
      name: 'Positive',
      xaxis: 'x3',
      yaxis: 'y',
      marker: {
        color: "#8CC234"
      },
      xbins: {
        size: 0.05
      }
    },
  ];

  const layout: Partial<Layout> = {
    title: 'Вероятность отнесения песни к эмоциональной окраске',
    grid: {
      rows: 1, 
      columns: 3, 
      // pattern: 'independent'
    },
    xaxis: {title: 'Негативная', range: [0, 1]},
    xaxis2: {title: 'Нейтральная', range: [0, 1] ,anchor: 'y'},
    xaxis3: {title: 'Позитивная', range: [0, 1] , anchor: 'y'},
    yaxis: {title: 'Количество песен'},
    showlegend: false
  };
  Plotly.newPlot(probabilitiesPlotElement.value, data, layout);
}

function getSentimentList(sentiment: 'negative'| 'positive'| 'neutral'): number[] {
  return fetchedSongsSentiment.value!.map(s => s[sentiment]);
}




</script>