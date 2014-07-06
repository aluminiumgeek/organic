/*
* app.js
* 
* Application config
*/

var app = angular.module('Farm', ['ngRoute', 'ngCookies']);

app.config(function($routeProvider, $httpProvider, $locationProvider) {
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    
    $routeProvider.
        when('/', {
            templateUrl: '/partials/login.html',
            controller: 'LoginCtrl',
        }).
        when('/panel', {
            templateUrl: '/partials/panel.html',
            controller: 'PanelCtrl'
        }).
        when('/users', {
            templateUrl: '/partials/users.html',
            controller: 'UsersCtrl'
        }).
        when('/logout', {
            templateUrl: '/partials/blank.html',
            controller: 'LogoutCtrl',
        })/*.
        otherwise({
            redirectTo: '/'
        });*/
        
    if (window.history && window.history.pushState) {
        $locationProvider.html5Mode(true);
    }
});

app.run(function($rootScope, $location, $cookies, $http) {
    $rootScope.$watch('token', function(val) {
        $http.defaults.headers.common.Authorization = 'Bearer ' + val;
    })
    
    if ($cookies.token) {
        $rootScope.token = $cookies.token;
        $rootScope.username = $cookies.username;
        $rootScope.is_staff = $cookies.is_staff == 'true'?true:false;
    }
    
    if (!$rootScope.token) {
        $location.path('/');
    }
    
    $rootScope.set_user = function(username) {
        $cookies.username = username;
        $rootScope.username = username;
    }
    $rootScope.set_token = function(token) {
        $cookies.token = token;
        $rootScope.token = token;
    }
    $rootScope.set_is_staff = function(is_staff) {
        $cookies.is_staff = is_staff;
        $rootScope.is_staff = is_staff;
    }

});
