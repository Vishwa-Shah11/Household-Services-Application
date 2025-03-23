<template>
    <div>
        <canvas ref="summaryChart"></canvas>
    </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
    data() {
        return {
            chart: null,
            chartData: null, // Holds the data from the API
        };
    },
    async mounted() {
        await this.fetchSummaryData();
        this.renderChart();
    },
    methods: {
        // async fetchSummaryData() {
        //     try {
        //         const token = localStorage.getItem("token"); // Get JWT from localStorage or Vuex
        //         if (!token) {
        //             console.error("No authentication token found.");
        //             return;
        //         }
        //         const response = await fetch("http://127.0.0.1:5858/professional/summary", {
        //             method: "GET",
        //             headers: {
        //                 "Authorization": `Bearer ${token}`, // Attach the token
        //                 "Content-Type": "application/json",
        //             },
        //         });
        //         if (!response.ok) {
        //             throw new Error(`HTTP Error: ${response.status}`);
        //         }
        //         const data = await response.json();
        //         console.log("API Data:", data);

        //         // Update chart data
        //         this.chartData = {
        //             labels: ["Requested", "Assigned", "Closed", "Rejected"],
        //             datasets: [
        //                 {
        //                     label: "Service Requests",
        //                     data: [data.requested, data.assigned, data.closed, data.rejected],
        //                     backgroundColor: ["blue", "green", "red", "orange"],
        //                 },
        //             ],
        //         };
        //     } catch (error) {
        //         console.error("Error fetching summary:", error);
        //     }
        // }
        // ,

        async fetchSummaryData() {
            try {
                const token = localStorage.getItem("token");
                if (!token) {
                    console.error("No authentication token found.");
                    return;
                }

                const response = await fetch("http://127.0.0.1:5858/professional/summary", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP Error: ${response.status}`);
                }

                const data = await response.json();

                // Print the response data in the console
                console.log("Fetched Data:", data);
                console.log("Requested:", data.Requested);
                console.log("Assigned:", data.Assigned);
                console.log("Closed:", data.Closed);
                console.log("Rejected:", data.Rejected);

                this.chartData = {
                    labels: ["Requested", "Assigned", "Closed", "Rejected"],
                    datasets: [
                        {
                            label: "Service Requests",
                            data: [data.Requested, data.Assigned, data.Closed, data.Rejected], // Debug this data
                            backgroundColor: ["blue", "green", "red", "orange"],
                        },
                    ],
                };

                console.log("Chart Data:", this.chartData);

            } catch (error) {
                console.error("Error fetching summary:", error);
            }
        },

        renderChart() {
            if (this.chart) this.chart.destroy(); // Destroy previous instance

            const ctx = this.$refs.summaryChart.getContext("2d");
            this.chart = new Chart(ctx, {
                type: "bar",
                data: this.chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            });
        },
    },
};
</script>