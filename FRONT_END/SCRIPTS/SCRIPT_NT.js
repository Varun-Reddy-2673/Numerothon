var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    if (typeof $cookies.Location == 'undefined') {
        window.location = 'HOME.html'
    }
    var Location = $cookies.Location;
    if (Location != 'NEW_TEST.html') {
        window.location = Location;
    }
    $scope.Information =  $cookies.Information.split (' | ');
    $scope.Request = {method: 'GET', url: 'REFRESH', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
    });
    $scope.Criteria = [[0, 0, 0], ['NOT SELECTED', 'NOT SELECTED', 'NOT SELECTED']];
    $scope.Request = {method: 'GET', url: 'NT_GET_GRADES', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
        var Records = response.data;
        $scope.Grades = Records.Grades;
    });
    $scope.Chapters = [];
    $scope.Change_Grade = function (Grade) {
        $scope.Request = {method: 'GET', url: 'NT_GET_CHANGE_GRADE/' + Grade, headers: {'Authorisation': $scope.Information [5]}};
        $http ($scope.Request).then (function (response) {
            if (response.data.Status == false) {
                window.location = 'SESSION.html'
            }
            var Records = response.data;
            $scope.Criteria = Records.Criteria;
            $scope.Chapters = Records.Chapters;
        });
    }
    $scope.Change_Chapter = function (Chapter_1, Chapter_2) {
        $scope.Request = {method: 'GET', url: 'NT_GET_CHANGE_CHAPTER/' + Chapter_1 + '/' + Chapter_2 + '/' + $scope.Criteria [0] [0] + '/' + $scope.Criteria [1] [0], headers: {'Authorisation': $scope.Information [5]}};
        $http ($scope.Request).then (function (response) {
            if (response.data.Status == false) {
                window.location = 'SESSION.html'
            }
            var Records = response.data;
            $scope.Criteria = Records.Criteria;
            $scope.Start_Test ()
        });
    }
    $scope.Start_Test = function () {
        var Parameters = {Account: $scope.Information [0], Chapter: $scope.Criteria [0] [1]};
        $scope.Request = {method: 'POST', url: 'NT_POST_CREATE_TEST', headers: {'Authorisation': $scope.Information [5]}, data: Parameters};
        $http ($scope.Request).then (function (response) {
            if (response.data.Status == false) {
                window.location = 'SESSION.html'
            }
            Records = response.data;
            $cookies.Test_Details = Records.ID + ' | ' + $scope.Criteria [0] [1];
            $cookies.Location = 'TEST.html';
            window.location = 'TEST.html'
        });
    }
    $scope.Change_Location = function (New_Location) {
        $cookies.Location = New_Location;
        window.location = New_Location;
    }
});
