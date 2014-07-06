/*
* app.js
* 
* Application config
*/

var app = angular.module('Farm', ['ngRoute']);

app.config(function($routeProvider, $locationProvider) {
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
        otherwise({
            redirectTo: '/'
        });
        
    if (window.history && window.history.pushState) {
        $locationProvider.html5Mode(true);
    }
});

app.run(function($rootScope) {
});
