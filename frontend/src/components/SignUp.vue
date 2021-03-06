<template>
    <div class="bg">
        <div class="sign-up">
            <div>
                <h2 id="title">注册</h2>
                <router-link to="/login" id="login-link">已有账号？</router-link>
            </div>
            <div class="form-panel">
                <div>
                    <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                        <Form-item label="邮箱" prop="account">
                            <Input placeholder="请输入注册邮箱或手机" v-model="formCustom.account"></Input>
                        </Form-item>
                        <Form-item label="用户名" prop="username">
                            <Input placeholder="请输入用户名" v-model="formCustom.username"></Input>
                        </Form-item>
                        <Form-item label="密码" prop="passwd">
                            <Input type="password" v-model="formCustom.passwd" placeholder="请输入密码"></Input>
                        </Form-item>
                        <Form-item label="确认密码" prop="passwdCheck">
                            <Input type="password" v-model="formCustom.passwdCheck" placeholder="请再次输入密码"></Input>
                        </Form-item>
                        <Form-item label="验证码" prop="vertification">
                            <Row>
                                <Col span="17">
                                <Input v-model="formCustom.verification" placeholder="请输入验证码"></Input>
                                </Col>
                                <Col span="7">
                                <Button type="ghost" @click="getVerification">获取验证码!</Button>
                                </Col>
                            </Row>
                        </Form-item>
                        <Form-item>
                            <Button type="primary" @click="signUp" id="signup-btn">确认注册</Button>
                        </Form-item>
                    </Form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
/**
 * 注册页面
 *
 * @module SignUp
 * @class SignUp
 */
import myMsg from './../warning.js'
export default {
    name: 'sign-up',
    data: function () {
        /**
         * 检验输入合法性
         *
         * @attribute validatePass
         * @readOnly
         */
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error(myMsg.account['passwordNeeded']))
            } else {
                if (this.formCustom.passwdCheck !== '') {
                    this.$refs.formCustom.validateField('passwdCheck')
                }
                callback()
            }
        }
        /**
         * 检验输入合法性
         *
         * @attribute validatePassCheck
         * @readOnly
         */
        const validatePassCheck = (rule, value, callback) => {
            if (value === '') {
                callback(new Error(myMsg.account['passwordAgain']))
            } else if (value !== this.formCustom.passwd) {
                callback(new Error(myMsg.account['passwordAgainWrong']))
            } else {
                callback()
            }
        }
        /**
         * 检验账号输入合法性
         *
         * @attribute validateAccount
         * @readOnly
         */
        const validateAccount = (rule, value, callback) => {
            let regMail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            let regPhone = /^1(3|4|5|7|8)\d{9}$/
            if (!value.match(regMail) && !value.match(regPhone)) {
                callback(new Error('请输入正确的账号'))
            } else {
                callback()
            }
        }
        return {
            /**
             * 检验输入合法性
             *
             * @attribute formCustom
             * @type Object
             */
            formCustom: {
                account: '',
                mailChecked: '',
                username: '',
                passwd: '',
                passwdCheck: '',
                vertification: '',
                loginKey: ''
            },
            /**
             * 检验输入合法性
             *
             * @attribute ruleCustom
             * @type Object
             */
            ruleCustom: {
                account: [
                    { required: true, message: '请输入邮箱或手机号', trigger: 'blur' },
                    { validator: validateAccount, trigger: 'blur' }
                ],
                username: [
                    { required: true, message: '请输入用户名！', trigger: 'blur' }
                ],
                passwd: [
                    { required: true, message: myMsg.account['passwordNeeded'], trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ],
                passwdCheck: [
                    { required: true, message: myMsg.account['passwordNeeded'], trigger: 'blur' },
                    { validator: validatePassCheck, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        /**
         * 获取验证码，调用getMailVerification或getPhoneVerification函数
         *
         * @method getVerification
         */
        getVerification: function () {
            if (this.checkEmailAndPhone() === 0) {
                return
            } else if (this.checkEmailAndPhone() === 1) {
                this.getMailVerification()
            } else if (this.checkEmailAndPhone() === 2) {
                this.getPhoneVerification()
            }
        },
        /**
         * 获取手机验证码
         *
         * @method getPhoneVerification
         */
        getPhoneVerification: function () {
            fetch('/getPhoneVerification/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'phoneNum': this.formCustom.account
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'exist') {
                    this.$Message.error(myMsg.account['accountExist'])
                    return
                }
                this.formCustom.loginKey = obj.verification
                this.formCustom.mailChecked = this.formCustom.account
                console.log(this.formCustom.loginKey)
            })
        },
        /**
         * 注册前进行输入有效性检查，
         * 当输入不合法时，弹出消息框提示。
         *
         * @method checkBeforeSignUp
         */
        checkBeforeSignUp: function () {
            if (this.formCustom.mailChecked !== this.formCustom.account) {
                this.$Message.error(myMsg.account['mailNotChange'])
                return false
            }
            if (this.formCustom.passwd === '') {
                this.$Message.error(myMsg.account['passwordNeeded'])
                return false
            }
            if (this.formCustom.passwd !== this.formCustom.passwdCheck) {
                this.$Message.error(myMsg.account['passwordAgainWrong'])
                return false
            }
            if (this.formCustom.username === '') {
                this.$Message.error(myMsg.account['nameNeeded'])
                return false
            }
            if (this.formCustom.verification === '') {
                this.$Message.error(myMsg.account['verificationNeeded'])
                return false
            }
            if (this.formCustom.verification !== this.formCustom.loginKey) {
                this.$Message.error(myMsg.account['verificationWrong'])
                return false
            }
            return true
        },
        /**
         * 进行注册
         *
         * @method signUp
         */
        signUp: function () {
            if (!this.checkBeforeSignUp()) {
                return
            }
            this.$Message.success(myMsg.account['signupSuccess'])
            fetch('/signUp/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'mail': this.formCustom.account,
                    'password': this.formCustom.passwd,
                    'username': this.formCustom.username
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result) {
                    this.$router.push({ path: '/login' })
                } else {
                    this.$Message.error(myMsg.account['nameExist'])
                }
            })
        },
        /**
         * 检查邮箱输入有效性
         *
         * @method checkEmail
         * @return true表示输入合法，false表示输入不合法，并弹出消息框
         */
        checkEmailAndPhone: function () {
            if (this.formCustom.account === '') {
                this.$Message.error('请输入邮箱或手机号')
                return 0
            }
            let regMail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            let regPhone = /^1(3|4|5|7|8)\d{9}$/
            if (this.formCustom.account.match(regMail)) {
                return 1
            } else if (this.formCustom.account.match(regPhone)) {
                return 2
            } else {
                this.$Message.error('请输入正确邮箱或手机号')
                return 0
            }
        },
        /**
         * 获取邮箱验证码
         *
         * @method getVerification
         */
        getMailVerification: function () {
            fetch('/getMailVerification/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'mail': this.formCustom.account })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'exist') {
                    this.$Message.error(myMsg.account['accountExist'])
                    return
                }
                this.formCustom.loginKey = obj.verification
                this.formCustom.mailChecked = this.formCustom.account
                console.log(this.formCustom.loginKey)
            })
        }
    }
}
</script>

<style scoped>
#title {
    font-size: x-large;
    position: absolute;
    margin-left: 222.5px;
    margin-top: -20px;
}

.sign-up {
    background-color: rgb(255, 255, 255);
    position: absolute;
    margin-left: -252.5px;
    left: 50%;
    margin-top: -284.5px;
    top: 50%;
    width: 505px;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0, 0, 0, .04);
    box-sizing: border-box;
    padding-top: 80px;
    padding-bottom: 60px;
}

.form-panel {
    margin-left: 12%;
    margin-right: 12%;
    margin-top: 40px;
}

.bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('./../assets/asteroids.jpg');
    background-repeat: repeat;
    z-index: -1;
    margin: auto;
}

#signup-btn {
    margin-left: -66px;
    margin-top: 30px;
}

#login-link {
    margin-right: -300px;
}
</style>
