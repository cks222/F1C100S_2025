<template>
    
    <RouterView />
</template>
<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>
<style>
* {
    margin: 0;
    padding: 0;
    font-family: "Source Sans Pro", sans-serif;
}

a:-webkit-any-link {
    text-decoration: none;
    color: black;
}

@font-face {
    font-family: 'Source Sans Pro';
    src: url('http://39.106.90.31/api/get_file?filepath=SourceSansPro-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}

.btn {
    cursor: pointer;
    color: rgb(49, 51, 63);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid gray;
    background-color: #F0F2F6;
}

.btn:hover {
    color: red;
    border-color: red;
}

.selectk {
    width: 300px;
    font-size: 25px;
    border-radius: 10px;
    padding: 3px;
}
</style>