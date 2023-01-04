var NUM_APP = angular.module ('NUM_APP', ['ngCookies']);
NUM_APP.controller ('NUM_CTRL', function ($scope, $http, $cookies) {
    if (typeof $cookies.Location == 'undefined') {
        window.location = 'HOME.html'
    }
    var Location = $cookies.Location;
    if (Location != 'TEST.html') {
        window.location = Location;
    }
    $cookies.Location = 'REPORTS.html'
    $scope.Information =  $cookies.Information.split (' | ');
    $scope.Request = {method: 'GET', url: 'REFRESH', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
    });
    $scope.Test_Details = $cookies.Test_Details.split (' | ');
    $scope.Counter = 0;
    $scope.Request = {method: 'GET', url: 'TE_GET_CREATE_BAR', headers: {'Authorisation': $scope.Information [5]}};
    $http ($scope.Request).then (function (response) {
        if (response.data.Status == false) {
            window.location = 'SESSION.html'
        }
        var Records = response.data;
        $scope.Correct_Array = Records.Correct_Array;
    });
    var New_Question = function () {
        var Parameters = {Chapter: $scope.Test_Details [1], Account: $scope.Information [0], Test: $scope.Test_Details [0]};
        $scope.Request = {method: 'POST', url: 'TE_POST_NEW_QUESTION', headers: {'Authorisation': $scope.Information [5]}, data: Parameters};
        $http ($scope.Request).then (function (response) {
            if (response.data.Status == false) {
                window.location = 'SESSION.html'
            }
            var Records = response.data;
            $scope.Question = Records.Question;
            $scope.Options = Records.Options.split (' | ');
            $scope.ID = Records.ID;
            $scope.Start_Time = Date.now ();
        });
    }
    New_Question ();
    $scope.Submit = function (Attempt) {
        var Time_Difference = Date.now () - $scope.Start_Time;
        var Parameters = {ID: $scope.ID, Attempt: Attempt, Time: Time_Difference};
        $scope.Request = {method: 'POST', url: 'TE_POST_SUBMIT_ANSWER', headers: {'Authorisation': $scope.Information [5]}, data: Parameters};
        $http ($scope.Request).then (function (response) {
            if (response.data.Status == false) {
                window.location = 'SESSION.html'
            }
            var Records = response.data;
            var Correct = Records.Correct;
            if (Correct == 1) {
                $scope.Correct_Array [$scope.Counter] = ['tick', 1];
            } else {
                $scope.Correct_Array [$scope.Counter] = ['cross', 0];
            }
            $scope.Counter += 1;
            if ($scope.Counter < 10) {
                $scope.Correct_Array [$scope.Counter] = ['current', 2];
                New_Question ();
            } else {
                window.location = 'REPORTS.html';
            }
            console.log ($scope.Correct_Array)
        });
    }
});
