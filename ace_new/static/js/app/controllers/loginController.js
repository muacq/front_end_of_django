function loginCtrl($scope, $http, $cookies) {
    $scope.initial = "initial";
    $scope.aa = "abc";
    $scope.cc = {};
    $scope.cc.a = "abc";

    $scope.account = {};

    console.log($scope.aa);
    console.log($scope.account);
    $scope.registerForm =function () {
        console.log($scope.account);
        $http({
            url: "/api/login/register",
            method: "post",
            data: $scope.account

        }).then(function (response) {
            console.log(response)
        })
    }
}