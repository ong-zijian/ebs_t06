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
    console.log("wordcloud is mounted")
    console.log("journalEntries", this.journalEntries)
    let width = 400;
    let height = 400;

    // Select the container in which to append the SVG
    let svg = d3.select(this.$refs.wordcloud).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Prepare the word data for the word cloud
    let wordCloudData = this.createWordFrequencyArray(this.journalEntries);

    // Set up the size scale for the word cloud
    let sizeScale = d3.scaleLinear()
      .domain([0, d3.max(wordCloudData, d => d.size)])
      .range([10, 100]); // Adjust min and max font sizes as needed

    // Create the word cloud layout and draw
    let layout = d3Cloud()
      .size([width, height])
      .words(wordCloudData)
      .padding(5)
      .rotate(() => 0) // Rotation of words; adjust as needed
      .font("Impact")
      .fontSize(d => sizeScale(d.size))
      .on("end", words => {
        svg.selectAll("text")
          .data(words)
          .enter().append("text")
          .style("font-size", d => d.size + "px")
          .style("fill", "#000") // Set the text color
          .attr("text-anchor", "middle")
          .attr("transform", d => `translate(${d.x}, ${d.y})rotate(${d.rotate})`)
          .text(d => d.text);
      });

    // Start the layout calculation
    layout.start();
  },
  methods: {
    useProp() {
      console.log("useProp is called")
      console.log("journalEntries", this.journalEntries)
    },
    createWordFrequencyArray(journalEntries) {
      if (!journalEntries){
        return [];
      } else {
        let allDescriptions = journalEntries.map(entry => entry.description).join(" ");
        let wordArray = allDescriptions.split(/\s+/);

        let wordFrequency = wordArray.reduce((accumulator, word) => {
          let cleanedWord = word.replace(/[^\w\s]|_/g, "").toLowerCase();
          if (cleanedWord && cleanedWord.length > 3) { // skip short words
            accumulator[cleanedWord] = (accumulator[cleanedWord] || 0) + 1;
          }
          return accumulator;
        }, {});

        return Object.keys(wordFrequency).map(word => {
          return { text: word, size: wordFrequency[word] };
        });
      }
    }
  }
}
</script>
  