<template>
    <div>
        <div class="panel">
            <panel-title title="任务详情">
                <el-button type="primary" size="small" @click="getTask">刷新</el-button>
            </panel-title>
            <div class="panel-body" v-if="taskInfo">
                <el-row v-if="taskInfo.status==0" style="text-align: center;">
                    <!-- <div class="circle-container" style="background-color: #444;">
                        <div class="radar"></div>
                    </div> -->
                    <div class="circle-container" style="background-color: #FFCCCC;">
                        <i class="fa fa-spin fa-cog"></i>
                    </div>
                    <div>
                        <p class="tip-title">正在初始化请稍后</p>
                    </div>
                </el-row>
                <el-row v-else-if="taskInfo.status==1" style="text-align: center;">
                    <div class="circle-container" style="background-color: #66CCFF;">
                        <i class="fa fa-inbox"></i>
                    </div>
                    <div>
                        <p class="tip-title">请连接数据源开始收集请求数据</p>
                        <p class="tip-desc" v-if="taskInfo.dataSource=='proxy'">
                            设置代理：
                            <span style="color:#FF6666;">{{taskInfo.dataSourceInfo.ip}}:{{taskInfo.dataSourceInfo.proxy}}</span>                            抓包详情：
                            <a class="out-link" :href="'http://'+taskInfo.dataSourceInfo.ip+':'+taskInfo.dataSourceInfo.web" target="_blank">{{taskInfo.dataSourceInfo.ip}}:{{taskInfo.dataSourceInfo.web}}</a>                            证书下载：
                            <el-tooltip class="item" effect="light" placement="right">
                                <div slot="content">请在代理设备上预先安装证书<br/>并且设置为 "受信任的根证书颁布机构"</div>
                                <a href="http://mitm.it" target="_blank" class="out-link">mitm.it</a>
                            </el-tooltip>
                        </p>
                        <el-button type="success" @click="startScan">开始扫描</el-button>
                        <el-button @click="cancelScan">取消扫描</el-button>
                    </div>
                </el-row>
                <el-row v-else-if="taskInfo.status==2" style="text-align: center;">
                    <div class="circle-container" style="background-color:#33CC33;">
                        <i class="fa fa-check"></i>
                    </div>
                    <div>
                        <p class="tip-title">扫描完成</p>
                        <router-link :to="{path: '/task/'+taskID+'/report'}" tag="span">
                            <el-button type="primary">查看报告</el-button>
                        </router-link>
                    </div>
                </el-row>
                <el-row v-else-if="taskInfo.status==3" style="text-align: center;">
                    <div class="circle-container" style="background-color: #FF3333;">
                        <i class="fa fa-exclamation"></i>
                    </div>
                    <div>
                        <p class="tip-title">初始化失败</p>
                    </div>
                </el-row>
                <el-row v-else-if="taskInfo.status==4" style="text-align: center;">
                    <div class="circle-container" style="background-color: #666666;">
                        <i class="el-icon-minus"></i>
                    </div>
                    <div>
                        <p class="tip-title">已取消扫描</p>
                    </div>
                </el-row>
                <el-row v-else-if="taskInfo.status==5" style="text-align: center;">
                    <!-- <div class="circle-container" style="background-color: #444;">
                        <div class="radar"></div>
                    </div> -->
                    <div class="circle-container" style="background-color: #FF9933;">
                        <i class="el-icon-loading"></i>
                    </div>
                    <div>
                        <p class="tip-title">正在扫描请稍后查看</p>
                    </div>
                </el-row>
            </div>
        </div>
        <el-card class="box-card" v-if="taskInfo">
            <el-row>
                <el-col :span="8">
                    <div class="info-title">数据源：</div>
                    <el-popover ref="datasourceinfo" placement="right-start" title="数据源信息" width="200" trigger="hover">
                        <pre style="line-height: 15px;font-size:14px;">{{obj2showString(taskInfo.dataSourceInfo)}}</pre>
                    </el-popover>
                    <div class="info-desc">{{taskInfo.dataSource}}
                        <el-button type="text" v-popover:datasourceinfo>详细</el-button>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="info-title">筛选规则：</div>
                    <el-popover ref="filterrule" placement="right-start" title="筛选规则" width="300" trigger="hover">
                        <pre style="line-height: 15px;font-size:14px;">{{arr2showString(taskInfo.filterRule)}}</pre>
                    </el-popover>
                    <div class="info-desc">{{taskInfo.filterRule.length}} 条
                        <el-button type="text" v-popover:filterrule>详细</el-button>
                    </div>
                </el-col>
                <el-col :span="8">
                    <div class="info-title">创建时间：</div>
                    <div class="info-desc">{{taskInfo.createTime}}
                        <el-button type="text">&nbsp;</el-button>
                    </div>
                </el-col>
            </el-row>
            <el-row style="margin-top:20px;">
                <el-col :span="24">
                    <div class="info-title">扫描项：</div>
                    <div class="info-desc">
                        <el-tag type="primary" v-for="poc in taskInfo.pocs" :key="poc.id" style="margin-right:5px;">{{poc.bugName}}</el-tag>
                    </div>
                </el-col>
            </el-row>
            <el-row style="margin-top:20px;">
                <el-col :span="24">
                    <div class="info-title">任务描述：</div>
                    <div class="info-desc">{{taskInfo.desc}}</div>
                </el-col>
            </el-row>
        </el-card>
    </div>
</template>

<script>
    import panelTitle from '../components/panelTitle'
    import api from '../api'
    import * as http from '../http'
    import '../assets/scanview.css'
    export default {
        data() {
            return {
                taskID: this.$route.params.id,
                taskInfo: null
            }
        },
        components: {
            panelTitle
        },
        methods: {
            getTask() {
                http.fetch(api.task(this.taskID)).then(data => {
                    this.taskInfo = data.data
                })
            },
            obj2showString(obj) {
                let kvarr = []
                for (let key in obj) {
                    kvarr.push(key + ' : ' + obj[key])
                }
                return kvarr.join('\n')
            },
            arr2showString(arr) {
                let temp = []
                for (let item of arr) {
                    temp.push(this.obj2showString(item))
                }
                return temp.join('\n-------------------------\n')
            },
            startScan() {
                this.$confirm('此操作将关闭释放数据源并开始扫描,请确认是否已断开数据源连接?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    http.post(api.task(this.taskID)).then(data => {
                        this.getTask()
                    })
                })
            },
            cancelScan() {
                this.$confirm('此操作将关闭释放数据源并取消扫描,请确认是否已断开数据源连接?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    http.del(api.task(this.taskID)).then(data => {
                        this.getTask()
                    })
                })
            }
        },
        created() {
            this.getTask()
            let timer = setInterval(() => {

                if (this.taskInfo && (this.taskInfo.status === 0 || this.taskInfo.status === 5)) {
                    this.getTask()
                } else if (this.taskInfo && (this.taskInfo.status === 2 || this.taskInfo.status === 3 || this.taskInfo
                        .status === 4)) {
                    clearInterval(timer)
                }
            }, 3000)
        }
    }

</script>

<style>
    .circle-container {
        font-size: 150px;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        text-align: center;
        line-height: 300px;
        color: #fff;
        margin: 20px auto 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    .tip-title {
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .tip-desc {
        font-size: 14px;
        color: #555;
        margin-bottom: 10px;
    }

    .info-title {
        font-size: 15px;
        font-weight: bold;
        width: 80px;
        display: inline-block;
    }

    .info-desc {
        font-size: 15px;
        display: inline-block;
    }

    .out-link:hover {
        color: #65cea7;
    }

    .out-link {
        color: #20a0ff;
    }

</style>
