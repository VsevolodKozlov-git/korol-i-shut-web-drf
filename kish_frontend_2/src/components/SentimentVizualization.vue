<template>

<v-card class="ma-10">
  <div ref="cntPlotElement"></div>
</v-card>

<v-card class="ma-10">
  <div ref="probabilitiesPlotElement"></div>
</v-card>


</template>


<script setup lang="ts">
import { onMounted, ref, watch} from 'vue';
import type { Ref } from 'vue'
import axios from 'axios';
import Plotly from 'plotly.js-dist-min'
import type {Data, Layout, Template} from 'plotly.js-dist-min';


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
albumsTitles: string[]
}>()

watch(() => props.albumsTitles, async () => {
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


const darkThemeTemplate = {
  layout: {
    paper_bgcolor: '#323232', // Background color of the outer area
    plot_bgcolor: '#323232', // Background color of the plotting area
    font: {
      color: '#7f7f7f' // Color of all the text
    },
    colorway: ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'], // Default set of colors for plots
    title: {
      font: {
        color: '#FFFFFF' // Specific color for title text
      }
    },
    xaxis: {
      tickfont: {
        color: '#7f7f7f'
      },
      title: {
        font: {
          color: '#7f7f7f'
        }
      }
    },
    yaxis: {
      tickfont: {
        color: '#7f7f7f'
      },
      title: {
        font: {
          color: '#7f7f7f'
        }
      }
    },
    legend: {
      font: {
        color: '#7f7f7f'
      }
    }
  }
};


function mergeLayouts(mainLayout:Partial<Layout>, themeLayout: Partial<Layout>): Partial<Layout>  {
    function mergeObjects(obj1:any, obj2:any) {
        Object.keys(obj2).forEach(key => {
            if (obj1.hasOwnProperty(key) && typeof obj1[key] === 'object' && typeof obj2[key] === 'object') {
                mergeObjects(obj1[key], obj2[key]);
            } else if (!obj1.hasOwnProperty(key)) {
                obj1[key] = obj2[key];
            }
        });
    }

    // Create a deep clone of the mainLayout to avoid modifying the original object
    let mergedLayout = JSON.parse(JSON.stringify(mainLayout));

    mergeObjects(mergedLayout, themeLayout);

    return mergedLayout;
}

const fetchedSongsSentiment: Ref<SongEntryFromGet[] | null> = ref(null);


// Function to fetch word frequency
async function fetchSongsSentiment() {
  let albumsTitles;
  if (props.albumsTitles.length > 0) {
    albumsTitles = props.albumsTitles.join() 
  }
  else {
    albumsTitles = 'sampletext'
  }
  
  try {
      const response = await axios.get<SongEntryFromGet[]>(`http://127.0.0.1:8000/app/vizualization/sentiment`, {
        params: { 
          albums_titles: albumsTitles
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
    title: {
      text:'Распределение песен по эмоциональной окраске'

    }
  }

  const mergedLayouts = mergeLayouts(layout, darkThemeTemplate.layout);

  Plotly.newPlot(cntPlotElement.value, data, mergedLayouts);
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
    title:{
      text: 'Вероятность отнесения песни к эмоциональной окраске'
    },
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
  const mergedLayout = mergeLayouts(layout, darkThemeTemplate.layout)
  Plotly.newPlot(probabilitiesPlotElement.value, data, mergedLayout);
}

function getSentimentList(sentiment: 'negative'| 'positive'| 'neutral'): number[] {
  return fetchedSongsSentiment.value!.map(s => s[sentiment]);
}




</script>