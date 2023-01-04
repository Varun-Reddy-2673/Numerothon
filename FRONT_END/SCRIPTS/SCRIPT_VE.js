var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    console.log (window.location.href)
    var Route = new URL (window.location.href)
    var Code = Route.searchParams.get ('Code')
    $scope.Status = true;
    $scope.Info = {}
    $http.get ('ACTIVATE/' + Code).then (function (response) {
        $scope.Status = response.data.Status;
        if ($scope.Status == true) {
            $scope.Info = response.data;
        } else {
            window.location = 'HOME.html';
        }
    });
    $scope.Continue = function () {
        $http.get ('SI_GET_ACCOUNT_INFO/' + $scope.Info.Username + '/' + $scope.Info.Password).then (function (response) {
            Records = response.data;
            if (Records.Message == '') {
                $cookies.Location = 'DASHBOARD.html';
                $cookies.Information = Records.Information;
                window.location = 'DASHBOARD.html';
            }
        });
    }
});