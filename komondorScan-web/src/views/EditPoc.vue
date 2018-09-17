<template>
    <div class="panel">
        <panel-title title="编辑 POC">
        </panel-title>
        <div class="panel-body">
            <el-row>
                <el-col :xs="24" :sm="24" :md="24" :lg="12">
                    <savePoc :poc="poc"></savePoc>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import panelTitle from '../components/panelTitle'
    import savePoc from './SavePoc'
    import api from '../api'
    import * as http from '../http'
    export default {
        data() {
            return {
                pocID: this.$route.params.id,
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
        },
        methods: {
            getPocInfo() {
                http.fetch(api.poc(this.pocID)).then(data => {
                    this.poc = data.data
                })
            }
        },
        created() {
            this.getPocInfo()
        }
    }

</script>

<style>


</style>
