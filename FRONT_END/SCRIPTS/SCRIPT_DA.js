var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    if (typeof $cookies.Location == 'undefined') {
        window.location = 'HOME.html'
    }
    var Location = $cookies.Location;
    if (Location != 'DASHBOARD.html') {
        window.location = Location;
    }
    $scope.Information =  $cookies.Information.split (' | ');
    $scope.Request = {method: 'GET', url: 'REFRESH', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
    });
    $scope.Change_Location = function (New_Location) {
        $cookies.Location = New_Location;
        window.location = New_Location;
    }
});