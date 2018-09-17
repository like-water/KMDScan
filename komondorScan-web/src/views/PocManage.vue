<template>
    <div class="panel">
        <panel-title title="POC 管理">
            <router-link :to="{path: '/pocs/add'}" tag="span">
                <el-button type="primary" icon="plus" size="small">创建 POC</el-button>
            </router-link>
        </panel-title>
        <div class="panel-body">
            <el-table :data="pocs" style="width: 100%" stripe>
                <el-table-column prop="bugName" label="BUG 名称">
                </el-table-column>
                <el-table-column prop="bugGrade" label="级别" width="100">
                    <template scope="scope">
                        <el-tag type="primary" v-if="scope.row.bugGrade==1" close-transition>低危</el-tag>
                        <el-tag type="warning" v-else-if="scope.row.bugGrade==2" close-transition>中危</el-tag>
                        <el-tag type="danger" v-else-if="scope.row.bugGrade==3" close-transition>高危</el-tag>
                        <el-tag type="gray" v-else>未知</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="pocDesc" label="描述">
                </el-table-column>
                <el-table-column label="操作" width="200">
                    <template scope="scope">
                        <router-link :to="{path: '/poc/'+scope.row.id+'/edit'}" tag="span">
                            <el-button type="info" size="small" icon="edit">修改</el-button>
                        </router-link>
                        <el-button type="danger" size="small" icon="delete" @click="deletePoc(scope.row.id)">删除</el-button>
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
                currentPageIndex: 1,
                pageSize: 10,
                totalCount: 0,
                pocs: []
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
            getPocs() {
                http.fetch(api.pocs, {
                    'pageSkip': this.pageSkip,
                    'pageTake': this.pageSize
                }).then(data => {
                    this.pocs = data.data.pageList
                    this.totalCount = data.data.totalCount
                })
            },
            handleSizeChange(val) {
                this.pageSize = val
                this.getPocs()
            },
            handleCurrentChange(val) {
                this.currentPageIndex = val
                this.getPocs()
            },
            deletePoc(id) {
                this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    http.del(api.poc(id)).then(data => {
                        this.getPocs()
                        this.$notify({
                            title: '成功',
                            message: 'POC删除成功',
                            type: 'success'
                        })
                    })
                })
            }
        },
        created() {
            this.getPocs()
        }
    }

</script>

<style>


</style>
