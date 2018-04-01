angular.module("myApp")
    .controller("questionDetailCtrl", questionDetailCtrl);

function questionDetailCtrl($scope, $http, $location) {
    $scope.question_detail = {};
    $scope.tags = [];
    $scope.full_content = "";
    $scope.mini_content = "";
    $scope.show_mini = true;
    $scope.question_liked = false;
    $scope.question_disliked = false;
    $scope.like_dislike_enabled = true;
    $scope.lock_button = false;
    $scope.question_answerd = false;
    $scope.token = localStorage.getItem("token");
    $scope.load_count =3;

    $scope.write_answer = false;
    $scope.answer_content = "";
    $scope.answer_warning = "";
    $scope.a_offset = 0;
    $scope.disable_scroll = false;
    $scope.answers = [];

    $scope.answers_like_statue = {};
    $scope.answers_dislike_statue = {};

    $scope.load_tag = function (question_id) {
        $http({
            url: "/api/tags/get_tags_by_question",
            method: "post",
            data: {
                qid: question_id
            }
        }).then(function (response) {
            $scope.tags = response.data.result;
        })
    };

    $scope.get_question = function () {
        $http({
            url: "/api/question/get_question",
            method: "post",
            data: {
                id: $scope.qid
            }
        }).then(function (response) {
            if(response.data.errors.length !== 0){
                if(response.data.errors[0] === "Question cannot be found"){
                    //TODO
                    window.location.href = "/";
                    return;
                }
            }
            $scope.question_detail = response.data.result;
            if($scope.question_detail.content.length > 50){
                $scope.mini_content = $scope.question_detail.content.substring(0, 50) + "...";
            }else{
                $scope.show_mini = false;
            }
            $scope.full_content = $scope.question_detail.content;
        })
    };

    $scope.get_question_status = function () {
        if(!$scope.token){
            return;
        }
        $http({
            url: "/api/post/has_like",
            method: "post",
            data: {
                _token: $scope.token,
                post_type: 1,
                target_id: $scope.qid
            }
        }).then(function (response) {
            $scope.question_liked = response.data.result;
            $scope.load_count--;
        });

        $http({
            url: "/api/post/has_dislike",
            method: "post",
            data: {
                _token: $scope.token,
                post_type: 1,
                target_id: $scope.qid
            }
        }).then(function (response) {
            $scope.question_disliked = response.data.result;
            $scope.load_count--
        });


        $http({
            url: "/api/post/has_answered",
            method: "post",
            data: {
                _token: $scope.token,
                post_type: 1,
                qid: $scope.qid
            }
        }).then(function (response) {
            $scope.question_answerd = response.data.result;
            $scope.load_count--
        })
    };

    $scope.load_answers = function (num) {
        $scope.disable_scroll = true;
        $http({
            url: "/api/question/get_answers",
            method: "post",
            data: {
                qid: $scope.qid,
                offset:$scope.a_offset,
                limit:num
            }
        }).then(function (response) {
            console.log(response);
            if(response.data.result.length === 0){
                return;
            }
            $scope.answers = $scope.answers.concat(response.data.result);
            $scope.a_offset += num;
            $scope.disable_scroll = false;
            if(!$scope.token){
                return;
            }
            angular.forEach(response.data.result, function (value) {
                $http({
                    url: "/api/post/has_like",
                    method: "post",
                    data: {
                        _token: $scope.token,
                        post_type: 2,
                        target_id: value.id
                    }
                }).then(function (response) {
                    $scope.answers_like_statue[value.id] = response.data.result;
                });

                $http({
                    url: "/api/post/has_dislike",
                    method: "post",
                    data: {
                        _token: $scope.token,
                        post_type: 2,
                        target_id: value.id
                    }
                }).then(function (response) {
                    $scope.answers_dislike_statue[value.id] = response.data.result;
                });
            });
        })
    };

    $scope.loadMore = function () {
        console.log(121);
        $scope.load_answers(5);
    };

    $scope.like_post = function (type, id, answer) {
        if(!$scope.token){
            //TODO
        }
        if(type === 1){
            id = $scope.qid;
        }
        if(!$scope.like_dislike_enabled)
            return;
        let liked = type === 1 ? $scope.question_liked : $scope.answers_like_statue[id];
        let disliked = type === 1 ? $scope.question_disliked : $scope.answers_dislike_statue[id];
        let count = type === 1 ? $scope.question_detail: answer;
        if(disliked){
            $scope.lock_button = true;
            $scope.dislike_post(type, id, answer);
        }
        $scope.like_dislike_enabled = false;
        if(liked){
            count.like_count--;
            if(type === 1){
                $scope.question_liked = false;
            }else{
                $scope.answers_like_statue[id] = false;
            }
            $http({
                url: "/api/question/unlike_post",
                method: "post",
                data: {
                    _token: $scope.token,
                    post_type: type,
                    target_id: id
                }
            }).then(function (response) {
                $scope.like_dislike_enabled = true;
            })
        }else{
            count.like_count++;
            if(type === 1){
                $scope.question_liked = true;
            }else{
                $scope.answers_like_statue[id] = true;
            }
            $http({
                url: "/api/question/like_post",
                method: "post",
                data: {
                    _token: $scope.token,
                    post_type: type,
                    target_id: id
                }
            }).then(function (response) {
                if($scope.lock_button){
                    $scope.lock_button = false;
                }else {
                    $scope.like_dislike_enabled = true;
                }
            })
        }
    };

    $scope.dislike_post = function (type, id, answer) {
        if(!$scope.token){
            //TODO
        }
        if(type === 1){
            id = $scope.qid;
        }
        if(!$scope.like_dislike_enabled)
            return;
        let liked = type === 1 ? $scope.question_liked : $scope.answers_like_statue[id];
        let disliked = type === 1 ? $scope.question_disliked : $scope.answers_dislike_statue[id];
        let count = type === 1 ? $scope.question_detail: answer;
        if(liked){
            $scope.lock_button = true;
            $scope.like_post(type, id, answer);
        }
        $scope.like_dislike_enabled = false;
        if(disliked){
            count.dislike_count--;
            if(type === 1){
                $scope.question_disliked = false;
            }else{
                $scope.answers_dislike_statue[id] = false;
            }
            $http({
                url: "/api/question/undislike_post",
                method: "post",
                data: {
                    _token: $scope.token,
                    post_type: type,
                    target_id: id
                }
            }).then(function (response) {
                $scope.like_dislike_enabled = true;
            })
        }else{
            count.dislike_count++;
            if(type === 1){
                $scope.question_disliked = true;
            }else{
                $scope.answers_dislike_statue[id] = true;
            }
            $http({
                url: "/api/question/dislike_post",
                method: "post",
                data: {
                    _token: $scope.token,
                    post_type: type,
                    target_id: id
                }
            }).then(function (response) {
                if($scope.lock_button){
                    $scope.lock_button = false;
                }else {
                    $scope.like_dislike_enabled = true;
                }
            })
        }
    };

    $scope.submit_answer = function () {
        if(!$scope.token){
            //TODO
        }
        if($scope.answer_content.length === 0){
            $scope.answer_warning = "答案内容不能为空";
            return;
        }
        $scope.question_answerd = true;
        $scope.write_answer = false;
        $http({
            url: "/api/question/answer_question",
            method: "post",
            data: {
                _token: $scope.token,
                qid: $scope.qid,
                content: $scope.answer_content
            }
        }).then(function (response) {

        });
    };

    $scope.init = function () {
        let path = $location.absUrl();
        let res = path.split("/");
        let x = 0;
        angular.forEach(res, function (value) {
            if(value === "question"){
                $scope.qid = res[x + 1]
            }
            x++;
        });
        $scope.get_question();
        $scope.load_tag($scope.qid);
        $scope.get_question_status();
        $scope.load_answers(10);
    };
    $scope.init();
}