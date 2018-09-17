<template>
    <div class="menu-right">
        <div class="notification-menu">
            <el-dropdown trigger="click" class="notification-list">
                <div class="notification-btn">
                    <span v-text="userName"></span>
                    <span class="icon"></span>
                </div>
                <el-dropdown-menu slot="dropdown" class="dropdown-menu">
                    <el-dropdown-item class="dropdown-list">
                        <a href="javascript:" class="dropdown-btn" @click="user_click(0)">
              <i class="icon fa fa-sign-out"></i>
              <span>安全退出</span>
            </a>
                    </el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>
    </div>
</template>
<script type="text/javascript">
    import {
        mapGetters
    } from 'vuex'
    const USER_OUT = 0

    export default {
        computed: {
            ...mapGetters(['userName'])
        },
        methods: {
            // 退出
            user_out() {
                this.$confirm('此操作将退出登录, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.$store.dispatch('setUserToken', '')
                }).catch(() => {

                })
            },
            user_info() {
                // 个人信息
            },
            user_setting() {
                // 设置
            },
            user_click(type) {
                switch (type) {
                    case USER_OUT:
                        // 退出
                        this.user_out()
                        break
                }
            }
        }
    }

</script>
