angular.module("myApp")
    .controller("exploreCtrl", exploreCtrl);

function exploreCtrl($scope, $http) {
    $scope.questions = [];
    $scope.q_offset = 0;
    $scope.tags = {};
    $scope.disable_scroll = false;

    $scope.load_tag = function (question_id) {
        $http({
            url: "/api/tags/get_tags_by_question",
            method: "post",
            data: {
                qid: question_id
            }
        }).then(function (response) {
            $scope.tags[question_id] = response.data.result;
        })
    };

    $scope.load_question = function (num) {
        $scope.disable_scroll = true;
        $http({
            url: "/api/question/get_questions",
            method: "post",
            data: {
                offset:$scope.q_offset,
                limit:num
            }
        }).then(function (response) {
            if(response.data.result.length === 0){
                return;
            }
            $scope.questions = $scope.questions.concat(response.data.result);
            $scope.q_offset += num;
            angular.forEach(response.data.result, function (value) {
                if(!$scope.tags[value.id]){
                    $scope.load_tag(value.id);
                }
            });
            $scope.disable_scroll = false;
        }, function (response) {
            console.log("fail:");
            console.log(response)
        });
    };

    $scope.init_all = function () {
        $scope.load_question(10);
    };

    $scope.find_tag = function (tag_id) {

    };

    $scope.loadMore = function () {
        $scope.load_question(5);
    };

    $scope.init_all();
}