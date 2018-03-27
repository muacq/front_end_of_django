angular.module("myApp")
    .controller("navCtrl", navCtrl);

function navCtrl($scope, $http) {
    $scope.post_ques_info = {};

    $scope.tags = null;

    $scope.tagging = [];

    $scope.title_warning = "";
    $scope.tag_warning = "";


    $scope.loadTags = function(query) {
        return $http({
            url: "/api/tags/query",
            method: "post",
            data: {
                keyword:query,
                tag_type:"",
                offset:0,
                limit:20
            }
        }).then(function (response) {
            var result = response.data.result;
            $scope.tagging = [];
            console.log(result);
            angular.forEach(result, function (value) {
                $scope.tagging.push({text:value.name,id:value.id});
            });
            return $scope.tagging;
        });
    };


    $scope.post_question = function () {
        $scope.title_warning = "";
        $scope.tag_warning = "";
        var pass = true;
        if($scope.post_ques_info.title === undefined || $scope.post_ques_info.title.length === 0){
            $scope.title_warning = "用户名不能为空";
            pass = false;
        }
        if($scope.tags === null || $scope.tags === undefined || $scope.tags.length === 0){
            $scope.tag_warning = "至少包含一个标签";
            pass = false;
        }
        if(!pass)
            return;

        var tags = [];
        angular.forEach($scope.tags, function (value) {
            tags.push(value.id);
        });
        $scope.post_ques_info.tags = JSON.stringify(tags);
        var token = localStorage.getItem("token");
        if(token){
            $scope.post_ques_info._token = token;
        }else{
            console.log(token);
        }
        $http({
            url: "/api/question/post_question",
            method: "post",
            data: $scope.post_ques_info
        }).then(function (response) {
            if(response.data.status === "OK"){
                $("#question-box").modal("hide");
                //TODO
            }else{

            }
        });
    }
}