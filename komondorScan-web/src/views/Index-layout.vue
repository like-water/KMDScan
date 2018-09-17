<template>
    <div class="view-page">
        <left-slide></left-slide>
        <main-content>
            <router-view></router-view>
        </main-content>
    </div>
</template>
<script type="text/javascript">
    import mainContent from '../components/mainContent'
    import leftSlide from '../components/leftSlide'

    export default {
        components: {
            mainContent,
            leftSlide
        }
    }

</script>
<style>


</style>
