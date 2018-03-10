angular.module("myApp")
    .controller("loginCtrl", loginCtrl);

function loginCtrl($scope, $http, $timeout) {
    $scope.account = {};
    $scope.agree = false;
    $scope.userMessage = "";
    $scope.emailMessage = "";
    $scope.passwordMessage = "";

    $scope.registerForm =function () {
        $timeout(function() {
            var username = $scope.account.username;
            var email = $scope.account.email;
            var password = $scope.account.password;

            var pass = true;
            $scope.userMessage = "";
            $scope.emailMessage = "";
            $scope.passwordMessage = "";
            if(username === undefined || username.length === 0){
                $scope.userMessage = "用户名不能为空";
                pass = false;
            }
            if(email === undefined || email.length === 0){
                $scope.emailMessage = "邮箱不能为空";
                pass = false;
            }
            if(password === undefined || password.length === 0){
                $scope.passwordMessage = "密码不能为空";
                pass = false;
            }
            var szReg = /^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,5}$/;
            if(!szReg.test(email)){
                $scope.emailMessage = "邮箱格式不正确";
                pass = false;
            }
            if(password.length < 6){
                $scope.passwordMessage = "password must contain at least 6 digits";
                pass = false;
            }
            if(!pass)
                return;

            $http({
                url: "/api/login/register",
                method: "post",
                data: $scope.account

            }).then(function (response) {
                console.log(response)
            });
        })
    };

    $scope.checkUsername = function () {
        var username = $scope.account.username;
        console.log(username);
        console.log(username.length);
        if(username === undefined || username.length === 0){
            $scope.userMessage = "用户名不能为空"
            return
        }
        $scope.userMessage = ""
    }
}