<template>
    <section class="body-warp">
        <transition name="fade" mode="out-in">
            <router-view></router-view>
        </transition>
    </section>
</template>

<script>
    export default {
        name: 'app'
    }

</script>

<style>


</style>
