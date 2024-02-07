<!-- <template>
  <div class="word-cloud-card">
    <div class="word-cloud-title"></div>
    <canvas ref="wordCloudHtmlElements[tagtype]" width="800px" height="400px"></canvas>
  </div>
</template>


<script setup>
import { onMounted, reactive, ref} from 'vue';
import WordCloud from 'wordcloud';


const props = defineProps({
  wordFrequency :{required: true},
  wordColor :{required: true}
})

function initWordCloud() {
  if (
    canvasElement.value!== null &&
    wordFrequency.all !== null &&
    wordColor.value !== null
  ){
    WordCloud(
      canvasElement.value, 
      {
        list: wordFrequency.all,
        color: (word) => wordColor[word],
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
}

// onMounted lifecycle hook
onMounted(
  initWordCloud
);
</script> -->