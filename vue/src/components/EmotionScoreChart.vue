<template>
    <div class="emotion-score-chart">
      <canvas ref="scoreChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  Chart.register(...registerables);
  
  export default {
    props: {
      plotData: Object
    },
    mounted() {
      Chart.register(...registerables);
      const ctx = this.$refs.scoreChart.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: this.plotData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              grid:{
                display: false
              }
            }
          },
          x:{
            grid:{
              display: false
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    }
  }
  </script>
  