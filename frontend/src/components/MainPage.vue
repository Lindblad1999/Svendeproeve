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
            let now = new Date();
            let year = now.getFullYear();
            let month = String(now.getMonth() + 1).padStart(2, '0');
            let day = String(now.getDate()).padStart(2, '0');
            let hours = String(now.getHours()).padStart(2, '0');
            let minutes = String(now.getMinutes()).padStart(2, '0');
            let seconds = String(now.getSeconds()).padStart(2, '0');
            this.dateTime = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
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