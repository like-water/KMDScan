<template>
    <div class="panel">
        <panel-title title="创建任务">
            <el-dropdown style="color:#73DAFF;">
                <span class="el-dropdown-link">
                    <i class="fa fa-question-circle"></i>
                    帮助
                </span>
                <el-dropdown-menu slot="dropdown" style="font-size:14px;">
                    <el-dropdown-item>
                        <a href="http://confluence.tech.apitops.com/pages/viewpage.action?pageId=8750196" target="_blank" style="color:#888">如何代理抓包</a>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </panel-title>
        <div class="panel-body">
            <el-row>
                <el-col :xs="24" :sm="24" :md="20" :lg="12">
                    <el-form label-width="80px">
                        <el-form-item label="任务描述">
                            <el-input v-model="form.desc"></el-input>
                        </el-form-item>
                        <el-form-item label="数据源">
                            <el-select v-model="form.dataSource" placeholder="请选择活动数据源">
                                <el-option label="代理" value="proxy"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="POCS">
                            <pocsSelect v-model="form.pocs"></pocsSelect>
                        </el-form-item>
                        <el-form-item label="筛选规则">
                            <el-row></el-row>
                            <el-row v-for="(rule, index) in form.filterRule" :key="index" :gutter="10" style="margin-bottom:10px;">
                                <el-col :span="6">
                                    <el-select placeholder="Type" v-model="rule.type">
                                        <el-option label="黑名单" value="blacklist"></el-option>
                                        <el-option label="白名单" value="whitelist"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="6">
                                    <el-select placeholder="Where" v-model="rule.where">
                                        <el-option label="URL" value="url"></el-option>
                                        <el-option label="Host" value="host"></el-option>
                                        <el-option label="Port" value="port"></el-option>
                                        <el-option label="Method" value="method"></el-option>
                                        <el-option label="Headers" value="headers"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="10">
                                    <el-input placeholder="RegEx" v-model="rule.regex"></el-input>
                                </el-col>
                                <el-col :span="2">
                                    <el-button type="text" icon="close" style="color:red;" @click="removeRule(index)"></el-button>
                                </el-col>
                            </el-row>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="createTask">创建</el-button>
                            <el-button @click="addRule">添加规则</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import panelTitle from '../components/panelTitle'
    import pocsSelect from '../components/pocsSelect'
    import api from '../api'
    import * as http from '../http'
    export default {
        data() {
            return {
                form: {
                    desc: '',
                    dataSource: 'proxy',
                    pocs: [],
                    filterRule: [
                        {
                            type: 'whitelist',
                            where: 'host',
                            regex:
                                '^[0-9a-zA-Z-]+\\.test\\.(apitops|topsboard)\\.com$'
                        },
                        {
                            type: 'whitelist',
                            where: 'port',
                            regex: '^(80|443)$'
                        }
                    ]
                }
            }
        },
        components: {
            panelTitle,
            pocsSelect
        },
        methods: {
            createTask() {
                http.post(api.tasks, this.form).then(data => {
                    this.$router.push({
                        path: '/task/' + data.data.data.taskID
                    })
                })
            },
            removeRule(index) {
                if (index !== -1) {
                    this.form.filterRule.splice(index, 1)
                }
            },
            addRule() {
                this.form.filterRule.push({
                    type: '',
                    where: '',
                    regex: ''
                })
            }
        }
    }
</script>

<style>

</style>
