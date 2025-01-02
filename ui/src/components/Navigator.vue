<template>
    <div class="nav">
        <router-link :to="{ name: 'chat' }" class="tab" active-class="active">Chat</router-link>
        <router-link :to="{ name: 'management' }" class="tab" active-class="active">Knowledge</router-link>
    </div>
    <hr>
</template>
<script setup lang="ts"></script>
<style scoped>
.nav {
    display: flex;
    justify-content: flex-start;
}

.tab {
    text-align: center;
    line-height: 30px;
    background-color: grey;
    text-decoration: none;
    min-width: 30px;
    padding: 0 10px ;
    border-radius: 0px 10px 0 0;
    cursor: pointer;
    color: black;
}

.active {
    background-color: gold;
}
</style>