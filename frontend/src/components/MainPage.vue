<template>
    <div>
        <h1>Smart Home Energy Meter</h1>
    </div>
    <div id="main-device">
        <div id="power-consumption-current">
            <h2 class="power-consumption-current-content">Current power consumption</h2>
            <p class="power-consumption-current-content">{{ latestWattage }} Watts</p>
        </div>
        <div id="energy-price">
            <h3 class="energy-price-content">Current energy price</h3>
            <p class="energy-price-content">{{ energyPrice }} kr. pr. kWh</p>
        </div>
        <div id="current-device-cost">
            <h3 class="current-device-cost-content">Current device cost</h3>
            <p class="current-device-cost-content">{{ deviceCost }} kr.</p>
        </div>
        <div id="total-device-cost">
            <h2 class="total-device-cost-content">Total device cost</h2>
            <p class="total-device-cost-content">{{ totalCost }} kr.</p>
        </div>
        <div id="relay-control">
            <button id="button-toggle" @click="toggleOnOff">{{ relayStatus }}</button>
        </div>
    </div>
</template>


<script>
import API_URL from '@/constants'
const DEVICE_ID = 2;
import axios from 'axios'
export default {
    data() {
        return {
            api_url: API_URL,
            dateTime: null,
            latestVoltage: 0,
            latestCurrent: 0,
            latestWattage: 0,
            energyPrice: 0,
            deviceCost: 0,
            totalCost: 0,
            relayStatus: "ON",
        };
    },
    mounted() {
        setInterval(this.getLatestWattage, 1000);
        this.getEnergyPrice();
        setInterval(this.currentDeviceCost, 1000);
        this.calcTotalCost();
        setInterval(this.updateTotalCost, 1000);
        setInterval(this.getRelayStatus, 1000);
    },
    methods:{
        getLatestWattage() {
            this.getLatestVoltage();
            this.getLatestCurrent();
            this.latestWattage = (this.latestVoltage * this.latestCurrent).toFixed(5);
        },
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
        getEnergyPrice() {
            let month = new Date().getMonth() + 1;
            let day = String(new Date().getDate()).padStart(2, '0');
            axios.get(`https://www.elprisenligenu.dk/api/v1/prices/2023/${month}-${day}_DK1.json`)
                .then(response => this.energyPrice = response.data[0].DKK_per_kWh)
        },
        currentDeviceCost() {
            let kwh = this.latestWattage / 3600;
            this.deviceCost = (kwh * this.energyPrice).toFixed(6);
        },
        calcTotalCost(){
            let getAmount = 100;

            // Use Promise to ensure that the API calls are completed before having to use the data they return
            Promise.all([
                axios.get(`${API_URL}/voltage/latest?amount=${getAmount}`),    
                axios.get(`${API_URL}/current/latest?amount=${getAmount}`)
            ]).then(([voltageResponse, currentResponse]) => {
                let topVoltages = voltageResponse.data;
                let topCurrents = currentResponse.data;
                let totalWattage = 0;
                for (let i = 0; i < getAmount; i++) {
                    totalWattage += topVoltages[i].meas * topCurrents[i].meas;
                }
                this.totalCost = (totalWattage / 3600) * this.energyPrice;
            })
        },
        updateTotalCost(){
            this.totalCost = (parseFloat(this.totalCost) + parseFloat(this.deviceCost)).toFixed(6);
        },
        toggleOnOff(){
            let postData= {
                state: this.relayStatus === "ON" ? 1 : 0, 
                device_id: DEVICE_ID
            };
            axios.post(`${API_URL}/relay/status`, postData);
        },
        getRelayStatus(){
            axios.get(`${API_URL}/relay/status`)
                .then( response => {
                    if (response.data.state){
                        this.relayStatus = "OFF";
                    } else {
                        this.relayStatus = "ON";
                    }
                })
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
    
    #power-consumption-current {
        background-color: gray;
        width: 70%;
        margin: 0 auto;
        border-radius: 25px;
    }
    
    .power-consumption-current-content {
        text-align: center;
    }

    #energy-price {
        background-color: gray;
        width: 40%;
        margin: 0 auto;
        border-radius: 20px;
    }

    .energy-price-content {
        text-align: center;
    }

    #current-device-cost {
        background-color: gray;
        width: 40%;
        margin: 0 auto;
        border-radius: 20px;
    }

    .current-device-cost-content {
        text-align: center;
    }

    #total-device-cost {
        background-color: darkred;
        width: 60%;
        margin: 0 auto;
        border-radius: 25px;
    }

    .total-device-cost-content {
        text-align: center;
    }

    #relay-control {
        display: flex;
        justify-content: center;
    }

    #button-toggle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
    }
</style>