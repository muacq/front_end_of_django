angular.module("myApp")
    .controller("loginCtrl", loginCtrl);

function loginCtrl($scope, $http, $timeout, $location) {
    $scope.switch = "";

    $scope.account_register = {};
    $scope.agree = false;
    $scope.userMessage_register = "";
    $scope.emailMessage_register = "";
    $scope.passwordMessage_register = "";
    
    $scope.account_login = {};
    $scope.userMessage_login = "";
    $scope.emailMessage_login = "";
    $scope.passwordMessage_login = "";

    $scope.registerForm =function () {
        $timeout(function() {
            var username = $scope.account_register.username;
            var email = $scope.account_register.email;
            var password = $scope.account_register.password;

            var pass = true;
            $scope.userMessage_register = "";
            $scope.emailMessage_register = "";
            $scope.passwordMessage_register = "";
            if(username === undefined || username.length === 0){
                $scope.userMessage_register = "用户名不能为空";
                pass = false;
            }
            if(email === undefined || email.length === 0){
                $scope.emailMessage_register = "邮箱不能为空";
                pass = false;
            }
            if(password === undefined || password.length === 0){
                $scope.passwordMessage_register = "密码不能为空";
                pass = false;
            }
            else if(password.length < 6){
                $scope.passwordMessage_register = "密码最少要包含6个字符";
                pass = false;
            }
            var szReg = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,5}$/;
            if(!szReg.test(email)){
                $scope.emailMessage_register = "邮箱格式不正确";
                pass = false;
            }

            if(!pass)
                return;

            $http({
                url: "/api/login/register",
                method: "post",
                data: $scope.account_register
            }).then(function (response) {
                localStorage.setItem("token", response.data.result._token);
                console.log(localStorage.getItem("token"));
            });
        })
    };

    $scope.loginForm =function () {
        $timeout(function() {
            var email = $scope.account_login.email;
            var password = $scope.account_login.password;

            var pass = true;
            $scope.emailMessage_login = "";
            $scope.passwordMessage_login = "";
            if(email === undefined || email.length === 0){
                $scope.emailMessage_login = "邮箱不能为空";
                pass = false;
            }
            if(password === undefined || password.length === 0){
                $scope.passwordMessage_login = "密码不能为空";
                pass = false;
            }
            var szReg = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,5}$/;
            if(!szReg.test(email)){
                $scope.emailMessage_login = "邮箱格式不正确";
                pass = false;
            }
            if(!pass)
                return;

            $http({
                url: "/api/login/login",
                method: "post",
                data: $scope.account_login
            }).then(function (response) {
                localStorage.setItem("token", response.data.result._token);
                window.location.href = "/";
            });
        })
    };

    $scope.turnToLogin = function () {
        $scope.switch = true;
    };

    $scope.turnToRegister = function () {
        $scope.switch = false;
    };

    var init = function () {
        var path = $location.absUrl();
        var logReg = /login/;
        var regReg = /register/;
        if(logReg.test(path)) {
            $scope.switch = true;
        }
        else if(regReg.test(path)){
            $scope.switch = false;
        }
        console.log($scope.switch)
        // if(path == "/login"){
        //     $scope.switch = true;
        // }
        // else if(path == "/register"){
        //     $scope.switch = false;
        // }
    };

    init();
}