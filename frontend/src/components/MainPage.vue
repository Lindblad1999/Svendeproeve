<template>
    <div>
        <h1>Smart Home Energy Meter</h1>
        <p>
            {{ voltage }}
        </p>
    </div>
</template>


<script>
import API_URL from '@/constants'
import axios from 'axios'
export default {
    data() {
        return {
            api_url: API_URL,
            dateTime: null,
            voltage: 0,
            value: 0
        };
    },
    mounted() {
        setInterval(this.getVoltage, 1000);
    },
    methods:{
        getVoltage() {
            this.dateTime = new Date().toISOString().replace(".", ":").slice(0, -5);
            axios.get(`${API_URL}/voltage/closest?timestamp=${this.dateTime}`)
                .then(response => this.voltage = response.data.meas)
            }
    }
}
</script>

<style>
    h1 {
        text-align: center;
    }
    p {
        text-align: center;
    }
</style>