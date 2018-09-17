<template>
    <div style="line-height: 1.2; height:100%">
        <codemirror :code="value" :options="editorOptions" @change="onEditorCodeChange">
        </codemirror>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                editorOptions: {
                    tabSize: 4,
                    mode: 'text/x-python',
                    theme: 'material',
                    lineNumbers: true,
                    line: true,
                    smartIndent: true,
                    lineWrapping: false
                }
            }
        },
        props: ['value'],
        methods: {
            onEditorCodeChange(newCode) {
                this.$emit('input', newCode)
            }
        }
    }

</script>

<style>
    .CodeMirror {
        height: 300px;
        min-height: 100%;
    }

</style>
