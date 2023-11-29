<template>
    <div>
        <h1>Smart Home Energy Meter</h1>
    </div>
    <div id="main-device">
        <div id="power-consumption-current">
            <h2 id="power-consumption">Current power consumption</h2>
            <p id="latest-wattage">{{ latestWattage }} Watts</p>
        </div>
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
            latestVoltage: 0,
            latestCurrent: 0,
            latestWattage: 0,
            value: 0
        };
    },
    mounted() {
        setInterval(this.getLatestWattage, 1000);
    },
    methods:{
        getLatestVoltage() {
            this.dateTime = new Date().toISOString().replace(".", ":").slice(0, -5);
            axios.get(`${API_URL}/voltage/closest?timestamp=${this.dateTime}`)
                .then(response => this.latestVoltage = response.data.meas)
        },
        getLatestCurrent() {
            this.dateTime = new Date().toISOString().replace(".", ":").slice(0, -5);
            axios.get(`${API_URL}/current/closest?timestamp=${this.dateTime}`)
                .then(response => this.latestCurrent = Math.abs(response.data.meas))
        },
        getLatestWattage() {
            this.getLatestVoltage();
            this.getLatestCurrent();
            console.log(`volt: ${this.latestVoltage}`)
            console.log(`current: ${this.latestCurrent}`)
            this.latestWattage = (this.latestVoltage * this.latestCurrent).toFixed(5);
        }
    }
}
</script>

<style>
    h1 {
        text-align: center;
    }

    #main-device {
        background-color: darkgrey;
        height: 50vh;
        width: 50vw;
        border-radius: 50px;
        border: 5px dotted;
        margin-left: 25%;
    }

    #latest-wattage {
        text-align: center;
    }

    #power-consumption {
        text-align: center;
    }

    #power-consumption-current {
        background-color: gray;
        width: 70%;
        margin: 0 auto;
        border-radius: 25px;
    }
</style>