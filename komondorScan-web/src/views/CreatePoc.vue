<template>
    <div class="panel">
        <panel-title title="创建 POC">
        </panel-title>
        <div class="panel-body">
            <el-row>
                <el-col :xs="24" :sm="24" :md="20" :lg="12">
                    <savePoc :poc="poc"></savePoc>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import panelTitle from '../components/panelTitle'
    import savePoc from './SavePoc'
    export default {
        data() {
            return {
                poc: {
                    bugName: '',
                    desc: '',
                    poc: '',
                    grade: ''
                }
            }
        },
        components: {
            panelTitle,
            savePoc
        }
    }

</script>

<style>


</style>
