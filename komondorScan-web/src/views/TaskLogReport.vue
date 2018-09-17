<template>
    <div class="panel">
        <panel-title title="扫描报告">
        </panel-title>
        <div class="panel-body">
            <div class="statistics-bar">
                统计数据
            </div>
            <div style="float:right;margin:10px 0;">
                <b style="font-size:15px;">显示错误</b>
                <el-switch
                    v-model="viewCode"
                    on-value="2"
                    off-value="1" @change="getTaskLogs">
                </el-switch>
            </div>
            <el-table :data="logs" style="width: 100%">
                <el-table-column type="expand">
                    <template scope="props">
                        <div>
                            <div class="detail-title">请求详情</div>
                            <pre class="detail-code">{{ jsonStringFormat(props.row.request) }}</pre>
                        </div>
                        <div>
                            <div class="detail-title">POC结果详情</div>
                            <pre>{{ props.row.resultDetail }}</pre>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="URL" prop="request.url">
                    <template scope="scope">
                        <el-tag type="danger" v-if="scope.row.code==2" close-transition>错误</el-tag>
                        {{scope.row.request.url}}
                    </template>
                </el-table-column>
                <el-table-column label="BUG 名称" prop="poc.bugName">
                    <template scope="scope">
                        <router-link :to="{path: '/poc/'+scope.row.poc.id+'/edit'}" tag="span">
                            <el-button type="text"> {{scope.row.poc.bugName}}</el-button>
                        </router-link>
                    </template>
                </el-table-column>
                <el-table-column label="危险级别" prop="poc.grade">
                    <template scope="scope">
                        <el-tag type="primary" v-if="scope.row.poc.grade==1" close-transition>低危</el-tag>
                        <el-tag type="warning" v-else-if="scope.row.poc.grade==2" close-transition>中危</el-tag>
                        <el-tag type="danger" v-else-if="scope.row.poc.grade==3" close-transition>高危</el-tag>
                        <el-tag type="gray" v-else>未知</el-tag>
                    </template>
                </el-table-column>
            </el-table>
            <bottomToolBar>
                <div slot="page">
                    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPageIndex" :page-size="pageSize"
                        layout="total,sizes, prev, pager, next" :total="totalCount" :page-sizes="[1, 10, 15, 25, 50]">
                    </el-pagination>
                </div>
            </bottomToolBar>
        </div>
    </div>
</template>

<script>
    import panelTitle from '../components/panelTitle'
    import bottomToolBar from '../components/bottomToolBar'

    import api from '../api'
    import * as http from '../http'
    export default {
        data() {
            return {
                taskID: this.$route.params.id,
                logs: [],
                currentPageIndex: 1,
                pageSize: 10,
                totalCount: 0,
                viewCode: 1
            }
        },
        components: {
            panelTitle,
            bottomToolBar
        },
        computed: {
            pageSkip() {
                return (this.currentPageIndex - 1) * this.pageSize
            }
        },
        methods: {
            getTaskLogs() {
                http.fetch(api.taskLog(this.taskID), {
                    'pageSkip': this.pageSkip,
                    'pageTake': this.pageSize,
                    'code': this.viewCode
                }).then(data => {
                    this.logs = data.data.pageList
                    for (let log of this.logs) {
                        log['request'] = JSON.parse(log.requestDetail)
                    }
                    this.totalCount = data.data.totalCount
                })
            },
            handleSizeChange(val) {
                this.pageSize = val
                this.getTaskLogs()
            },
            handleCurrentChange(val) {
                this.currentPageIndex = val
                this.getTaskLogs()
            },
            jsonStringFormat(json) {
                return JSON.stringify(json, null, 2)
            }
        },
        created() {
            this.getTaskLogs()
        }
    }

</script>

<style>
    .detail-title {
        padding: 10px 0px;
        font-weight: bold;
    }

    .detail-code {
        color: red;
        white-space: pre-wrap;
        white-space: -moz-pre-wrap;
        white-space: -pre-wrap;
        white-space: -o-pre-wrap;
        word-wrap: break-word;
    }

    .statistics-bar {
        padding-bottom: 10px;
        font-size: 14px;
    }

</style>
