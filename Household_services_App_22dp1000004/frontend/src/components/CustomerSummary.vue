<template>
    <div class="container">
      <h2>Service Requests</h2>
      <canvas id="customerChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, BarElement, CategoryScale, LinearScale, BarController } from 'chart.js';
  import axios from 'axios';
  
  Chart.register(BarElement, CategoryScale, LinearScale, BarController);
  
  export default {
    data() {
      return {
        chart: null,
        serviceData: {
          requested: 0,
          assigned: 0,
          closed: 0
        }
      };
    },
    mounted() {
      this.fetchSummary();
    },
    methods: {
      async fetchSummary() {
        try {
          const response = await axios.get('http://127.0.0.1:5858/customer/summary', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.serviceData = response.data;
          this.renderChart();
        } catch (error) {
          console.error("Error fetching summary:", error);
        }
      },
      renderChart() {
        if (this.chart) this.chart.destroy(); // Destroy old chart if exists
  
        const ctx = document.getElementById("customerChart").getContext("2d");
        this.chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: ["Requested", "Assigned", "Closed"],
            datasets: [
              {
                label: "Service Requests",
                data: [this.serviceData.requested, this.serviceData.assigned, this.serviceData.closed],
                backgroundColor: ["#74b9ff", "#ff7675", "#55efc4"],
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    text-align: center;
    width: 60%;
    margin: auto;
  }
  </style>
  