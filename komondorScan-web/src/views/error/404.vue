<template>
    <div class="error-page">
        <div class="errorWarp">
            <div class="image">
                <img :src="image">
            </div>
            <h2 class="title" v-text="title"></h2>
            <h3 class="desc" v-text="desc"></h3>
            <router-link :to="path" class="backBtn" tag="span">返回首页</router-link>
        </div>
    </div>
</template>
<script type="text/javascript">
    export default {
        name: 'noPage',
        data() {
            return {
                image: require('./images/404_error.png'),
                title: 'PAGE NOT FOUND',
                desc: '您访问的页面已经打酱油去了',
                path: '/'
            }
        }
    }

</script>
<style>
    .error-page {
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: #6bc5a4;
        text-align: center;
    }

    .error-page .errorWarp {
        width: 1000px;
        margin: 10% auto auto auto;
    }

    .error-page .errorWarp .image {
        margin: 20px auto;
    }

    .error-page .errorWarp .title {
        color: #fff;
        font-size: 64px;
        padding: 15px 30px;
        margin-bottom: 20px;
        margin-top: 50px;
        font-weight: bold;
    }

    .error-page .errorWarp .desc {
        font-size: 32px;
        color: #474747;
        font-weight: bold;
        line-height: 30px;
    }

    .error-page .errorWarp .backBtn {
        display: inline-block;
        color: #fff;
        margin-bottom: 20px;
        margin-top: 50px;
        padding: 15px 30px;
        border: 1px solid #fff;
        border-radius: 5px;
        cursor: pointer;
    }

</style>
