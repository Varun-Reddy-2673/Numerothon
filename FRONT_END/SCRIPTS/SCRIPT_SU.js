var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    $scope.Modal_Information = {Type: '', Message: ''};
    $scope.Submit = function () {
        $http.post ('SU_POST_CREATE_ACCOUNT', $scope.Values).then (function (response) {
            $scope.Modal_Information = response.data;
            $http.post ('SU_POST_VERIFY', {E_Mail: $scope.Values.E_Mail}).then (function () {});
        });
    }
});