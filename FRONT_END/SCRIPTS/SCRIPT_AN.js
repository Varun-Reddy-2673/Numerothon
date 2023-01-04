var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    if (typeof $cookies.Location == 'undefined') {
        window.location = 'HOME.html'
    }
    var Location = $cookies.Location;
    if (Location != 'ANALYSIS.html') {
        window.location = Location;
    }
    $scope.Information =  $cookies.Information.split (' | ');
    $scope.Request = {method: 'GET', url: 'REFRESH', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
    });
    $scope.Request = {method: 'GET', url: 'AN_GET_TESTS/' + $scope.Information [0], headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html';
        } else {
            var Tests = response.data.Tests;
            var Values = [];
            var Infos = [[], [], []];
            for (Test in Tests) {
                var Value = Tests [Test] [2];
                Values.push ([parseInt (Value * 16 / 5), 400 - parseInt (Value * 16 / 5), parseInt (Test * 80 + 65)])
                Infos [0].push ([Test * 80 + 60, Tests [Test] [4]]);
                Infos [1].push ([Tests [Test] [1], Tests [Test] [4]]);
                Infos [2].push ([Tests [Test] [3], Tests [Test] [4]]);
            }
            $scope.Graphs = Values;
            $scope.Infos_1 = Infos [0];
            $scope.Infos_2 = Infos [1];
            $scope.Infos_3 = Infos [2];
        }
    });
    $scope.Change_Location = function (New_Location) {
        $cookies.Location = New_Location;
        window.location = New_Location;
    }
});