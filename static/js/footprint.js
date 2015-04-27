var app = angular.module('FootPrint', []);
app.controller("PageControl", function ($scope, $http, $window) {
    $scope.view = {
        getView: function() {
            return "login.html";
        }
    };
    $scope.UserLoggedIn = function () { 
    	console.log("userlogin is ");
    	console.log($window.sessionStorage.getItem('token') != null);
    	   return $window.sessionStorage.getItem('token') != null;
    };
    $scope.submit = function () {
        console.log($scope.user);
        $http({
            method  : 'POST',
            url     : 'getToken',
            data    : $.param($scope.user),  // pass in data as strings
            headers : { 'Content-Type': 'application/x-www-form-urlencoded' }  // set the head
        }).success(function (data, status, headers, config) {
            $window.sessionStorage.token = data.token;
            alert("Token: " + data.token);
        })
            .error(function (data, status, headers, config) {
                // Erase the token if the user fails to log in
                delete $window.sessionStorage.token;

                // Handle login errors here
                $scope.message = 'Error: Invalid user or password';
            });
    };
});

app.factory('authInterceptor', function ($rootScope, $q, $window) {
    return {
        request: function (config) {
            config.headers = config.headers || {};
            if ($window.sessionStorage.token) {
                config.headers.Authorization = $window.sessionStorage.token;
            }
            return config;
        },
        response: function (response) {
            if (response.status === 401) {
                // handle the case where the user is not authenticated
            }
            return response || $q.when(response);
        }
    };
});

app.config(function ($httpProvider) {
    $httpProvider.interceptors.push('authInterceptor');
});



