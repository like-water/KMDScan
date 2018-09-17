<template>
    <el-form ref="poc" :model="poc" label-width="80px">
        <el-form-item label="BUG 名称">
            <el-input v-model="poc.bugName"></el-input>
        </el-form-item>
        <el-form-item label="危险级别">
            <el-select v-model="poc.grade" placeholder="请选择安全级别">
                <el-option v-for="item in bugGrade" :label="item.lable" :value="item.value" :key="item.value"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="POC 描述">
            <el-input type="textarea" v-model="poc.desc" :autosize="{minRows: 3}"></el-input>
        </el-form-item>
        <el-form-item label="POC">
            <codeTestArea v-model="poc.poc" style="height:500px;"></codeTestArea>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSave">保存</el-button>
        </el-form-item>
    </el-form>
</template>

<script>
    import codeTestArea from '../components/codeTestArea'
    import api from '../api'
    import * as http from '../http'
    export default {
        data() {
            return {
                bugGrade: [{
                    lable: '低',
                    value: 1
                }, {
                    lable: '中',
                    value: 2
                }, {
                    lable: '高',
                    value: 3
                }]
            }
        },
        props: ['poc'],
        components: {
            codeTestArea
        },
        methods: {
            onSave() {
                console.log(this.poc)
                if (this.poc.id) {
                    http.put(api.poc(this.poc.id), this.poc).then(data => {
                        this.$notify({
                            title: '成功',
                            message: 'POC保存成功',
                            type: 'success'
                        })
                        this.$router.push({
                            path: '/pocs'
                        })
                    })
                } else {
                    http.post(api.pocs, this.poc).then(data => {
                        this.$notify({
                            title: '成功',
                            message: 'POC保存成功',
                            type: 'success'
                        })
                        this.$router.push({
                            path: '/pocs'
                        })
                    })
                }
            }
        }
    }

</script>

<style>


</style>
