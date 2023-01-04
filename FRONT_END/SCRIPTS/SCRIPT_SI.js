var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    $scope.Message = '';
    $scope.Submit = function () {
        $http.get ('SI_GET_ACCOUNT_INFO/' + $scope.Username + '/' + $scope.Password).then (function (response) {
            Records = response.data;
            $scope.Message = Records.Message;
            if (Records.Message == '') {
                $cookies.Location = 'DASHBOARD.html';
                $cookies.Information = Records.Information;
                window.location = 'DASHBOARD.html';
            }
        });
    }
});