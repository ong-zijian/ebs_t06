<template>
    <div ref="wordcloud"></div>
  </template>
  
  <script>
  import * as d3 from 'd3';
  import d3Cloud from 'd3-cloud';
  
  export default {
    props: {
      journalEntries: Array
    },
    mounted() {
      let wordCloudData = this.createWordFrequencyArray(this.journalEntries);
      // ... Set up dimensions, SVG, and word cloud layout as previously described ...
    },
    methods: {
      createWordFrequencyArray(journalEntries) {
        // ... Same method as before ...
      }
    }
  }
  </script>
  