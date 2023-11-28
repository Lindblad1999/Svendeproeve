<template>
    <div>
        <h1 style="margin-left: 40%;">Smart Home Energy Meter</h1>
        <p>
            {{ info }}
        </p>
    </div>
    <div>
        <form @submit.prevent="setApiAddress">
            <label>API IP Address:</label>
            <input type="text" v-model="apiInput">
            <button type="submit">Set</button>
        </form>
    </div>
</template>


<script>
// import TEST_API from '@/constants'

import axios from 'axios'
export default {
    data() {
        return {
            apiInput: '',
            apiAddress: '',
            info: null
        };
    },
    methods:{
        setApiAddress() {
            this.apiAddress = this.apiInput;
            axios.get(`http://${this.apiAddress}`)
                .then(response => this.info = response.data)
        },
        // getVoltage() {
        //     axios.get('${this.apiAddress}/voltage')
        //         .then(response => this.info = response)
        // }
    }
}
</script>