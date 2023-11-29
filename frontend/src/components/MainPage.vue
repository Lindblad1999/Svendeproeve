<template>
    <div>
        <h1 style="margin-left: 40%;">Smart Home Energy Meter</h1>
        <p>
            {{ info }}
        </p>
    </div>
</template>


<script>
import API_URL from '@/constants'
import axios from 'axios'
export default {
    data() {
        return {
            info: null
        };
    },
    methods:{

        // getVoltage() {
        //     axios.get('${this.apiAddress}/voltage')
        //         .then(response => this.info = response)
        // }
    }
}
</script>