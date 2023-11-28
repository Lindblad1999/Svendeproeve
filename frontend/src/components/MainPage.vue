<template>
    <div>
        <h1>MAIN PAGE</h1>
        <p style="margin-left: 50%;">
            {{ info }}
        </p>
    </div>
</template>


<script>
import TEST_API from '@/constants'

import axios from 'axios'
export default {
    data() {
        return {
            info: null
        };
    },
    mounted() {
        axios
            .get(TEST_API)
            .then(response => (this.info = response.status))
    }
}
</script>