<template>
    <div>
        <h2>Admin Summary</h2>
        <div>
            <h3>User Summary</h3>
            <div class="chart-container">
                <canvas id="userChart"></canvas>
            </div>
        </div>
        <div>
            <h3>Service Analytics</h3>
            <div class="chart-container">
                <canvas id="serviceChart"></canvas>
            </div>
        </div>
    </div>
</template>


<script>
import { defineComponent, onMounted, ref, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import axios from 'axios';

export default defineComponent({
    name: 'AdminSummaryChart',
    setup() {
        const userSummary = ref(null);
        const serviceSummary = ref(null);
        const userChartInstance = ref(null);
        const serviceChartInstance = ref(null);

        const fetchSummaryData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5858/admin/summary');
                userSummary.value = response.data.userSummary;
                serviceSummary.value = response.data.serviceSummary;

                await nextTick(); // Wait for DOM update
                renderUserChart();
                renderServiceChart();
            } catch (error) {
                console.error('Error fetching summary data:', error);
            }
        };

        const renderUserChart = () => {
            const ctx = document.getElementById('userChart')?.getContext('2d');
            if (!ctx || !userSummary.value) return;

            if (userChartInstance.value) {
                userChartInstance.value.destroy();
            }
            userChartInstance.value = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Customers', 'Approved Professionals', 'Rejected Professionals'],
                    datasets: [
                        {
                            label: 'User Breakdown',
                            data: [
                                userSummary.value.customerCount,
                                userSummary.value.approvedProfessionalCount,
                                userSummary.value.rejectedProfessionalCount
                            ],
                            backgroundColor: ['blue', 'green', 'red']
                        }
                    ]
                }
            });
        };

        const renderServiceChart = () => {
            const ctx = document.getElementById('serviceChart')?.getContext('2d');
            if (!ctx || !serviceSummary.value) return;

            if (serviceChartInstance.value) {
                serviceChartInstance.value.destroy();
            }
            serviceChartInstance.value = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(serviceSummary.value),
                    datasets: [
                        {
                            label: 'Service Categories',
                            data: Object.values(serviceSummary.value),
                            backgroundColor: 'purple'
                        }
                    ]
                }
            });
        };

        onMounted(fetchSummaryData);

        return { userSummary, serviceSummary };
    }
});

</script>

<style scoped>
h1,
h2 {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 10px;
}

div {
    margin-bottom: 20px;
}

/* canvas {
    width: 100% !important;
    max-width: 500px;
    height: 300px !important;
} */

canvas {
    max-width: 400px;
    max-height: 400px;
}

.chart-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}
</style>