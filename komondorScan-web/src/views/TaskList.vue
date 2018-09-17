<template>
    <div class="panel">
        <panel-title title="任务列表">
        </panel-title>
        <div class="panel-body">
            <el-table :data="tasks" style="width: 100%" stripe @row-click="gotoDetail">
                <el-table-column prop="status" label="任务状态" width="100">
                    <template scope="scope">
                        <el-tag type="warning" v-if="scope.row.status==0" close-transition>正在初始化</el-tag>
                        <el-tag type="primary" v-if="scope.row.status==1" close-transition>待扫描</el-tag>
                        <el-tag type="success" v-else-if="scope.row.status==2" close-transition>扫描完成</el-tag>
                        <el-tag type="danger" v-else-if="scope.row.status==3" close-transition>初始化失败</el-tag>
                        <el-tag type="gray" v-else-if="scope.row.status==4" close-transition>已取消</el-tag>
                        <el-tag type="warning" v-else-if="scope.row.status==5" close-transition>正在扫描</el-tag>
                        <el-tag type="gray" v-else>未知</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="desc" label="任务描述">
                </el-table-column>
                <el-table-column prop="createTime" label="创建时间" width="200">
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
                currentPageIndex: 1,
                pageSize: 10,
                totalCount: 0,
                tasks: []
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
            getTasks() {
                http.fetch(api.tasks, {
                    'pageSkip': this.pageSkip,
                    'pageTake': this.pageSize
                }).then(data => {
                    this.tasks = data.data.pageList
                    this.totalCount = data.data.totalCount
                })
            },
            handleSizeChange(val) {
                this.pageSize = val
                this.getTasks()
            },
            handleCurrentChange(val) {
                this.currentPageIndex = val
                this.getTasks()
            },
            gotoDetail(row) {
                if (row.status === 2) {
                    this.$router.push({
                        path: '/task/' + row.id + '/report'
                    })
                } else {
                    this.$router.push({
                        path: '/task/' + row.id
                    })
                }
            }
        },
        created() {
            this.getTasks()
        }
    }

</script>

<style>


</style>
