<template>
    <el-select v-model="selects" multiple filterable placeholder="请选择" style="width:100%">
        <el-option v-for="item in pocs" :key="item.id" :label="item.bugName" :value="item.id">
        </el-option>
    </el-select>
</template>

<script>
    import api from '../api'
    import * as http from '../http'
    export default {
        data() {
            return {
                pocs: [],
                selects: []
            }
        },
        props: ['value'],
        methods: {
            getPocSelectList() {
                http.fetch(api.pocsForSelect).then(data => {
                    this.pocs = data.data
                })
            }
        },
        created() {
            this.getPocSelectList()
        },
        watch: {
            selects() {
                this.$emit('input', this.selects)
            },
            value() {
                this.selects = this.value
            }
        }
    }

</script>

<style>


</style>
