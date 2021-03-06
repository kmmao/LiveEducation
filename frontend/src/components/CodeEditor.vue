<template>
    <div id="code-editor">
        <Select id="language-selector" v-model='editorOptions.mode' placeholder="language" filterable>
            <Option v-for='mode in modeList' :value='mode.modeValue' :key='mode.modeName'>
                {{ mode.modeName }}
            </Option>
        </Select>
        <codemirror id='code' v-model='code' :options='editorOptions'></codemirror>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 实现教学区代码编辑器功能，
 * 作为子组件插入直播间页面。
 * 老师端可以选择不同语言输入代码，
 * 并同步到学生端。
 * 学生端不能对代码编辑器进行操作，
 * 只能同步看到老师的操作。
 *
 * @module CodeEditor
 * @class CodeEditor
 */
import * as io from 'socket.io-client'
export default {
    name: 'code-editor',
    /**
     * 表示房间ID信息
     *
     * @property roomId
     * @type String
     */

    /**
     * 表示创建该房间的老师名字
     *
     * @property teacherName
     * @type String
     */

    /**
     * 表示进入该房间的用户名字
     *
     * @property username
     * @type String
     */

    /**
     * 表示教学区域的高，根据父组件大小动态变化
     *
     * @property containerHeight
     * @type Number
     */

    /**
     * 表示代码编辑器是否位于左边窗口
     *
     * @property isOnLeft
     * @type Boolean
     */
    props: ['roomId', 'teacherName', 'username', 'containerHeight', 'isOnLeft'],
    data: function () {
        return {
            /**
             * 表示编辑器中输入的代码
             *
             * @attribute code
             * @type String
             */
            code: '',
            /**
             * 编辑器中的一些设置参数
             *
             * @attribute editorOptions
             * @type Object
             */
            editorOptions: {
                readOnly: false,
                tabSize: 4,
                mode: 'text/javascript',
                theme: 'base16-dark',
                lineNumbers: true,
                line: true,
                keyMap: 'sublime',
                extraKeys: { 'Ctrl': 'autocomplete' },
                foldGutter: true,
                gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
                styleSelectedText: true,
                highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true }
            },
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            /**
             * 表示语言选择的列表
             *
             * @attribute modeList
             * @type Array
             */
            modeList: [
                {
                    modeName: 'JavaScript',
                    modeValue: 'text/javascript'
                },
                {
                    modeName: 'C/C++',
                    modeValue: 'text/x-c++src'
                },
                {
                    modeName: 'C#',
                    modeValue: 'text/x-csharp'
                },
                {
                    modeName: 'Java',
                    modeValue: 'text/x-java'
                },
                {
                    modeName: 'PHP',
                    modeValue: 'text/x-php'
                }
            ]
        }
    },
    /**
     * mounted函数，连接到socket服务器，并初始化相关数据。
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinForCodeEditor', self.roomId + '.3')
        if (self.username !== self.teacherName) {
            self.editorOptions.readOnly = true
            self.socket.on('message', function (data) {
                self.code = data['code']
            })
        }
        document.getElementsByClassName('CodeMirror')[0].style.maxHeight = (this.containerHeight - 32) + 'px'
    },
    watch: {
        code: function (newcode, oldcode) {
            if (newcode !== oldcode && this.username === this.teacherName) {
                this.socket.emit('message', {
                    type: 'code',
                    code: newcode
                }, this.roomId + '.3')
            }
        },
        containerHeight: function (newVal, oldVal) {
            document.getElementsByClassName('CodeMirror')[0].style.maxHeight = (this.containerHeight - 32) + 'px'
        }
    }
}
</script>

<style scoped>
#code-editor {
    width: 100%;
    height: auto;
    text-align: left;
}
</style>
