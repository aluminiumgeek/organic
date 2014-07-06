/*
 * Controllers 
 * 
 */

app.controller('LoginCtrl', function($scope, $http, $rootScope, $location) {
    if ($rootScope.token) {
        $location.path('/panel');
    }
    
    $scope.submit = function() {
        $http({
            url: '/api/user/auth',
            method: 'post',
            data: utils.param($scope.model)
        }).success(function(data) {
            if (data.status == 'error') {
                $scope.warning = data.msg;
            }
            else {
                $rootScope.set_user(data.username);
                $rootScope.set_token(data.token);
                $rootScope.set_is_staff(data.is_staff);
                
                $location.path('/panel');
            }
        })
    }
});

app.controller('LogoutCtrl', function($scope, $rootScope, $http, $location) {

    if ($rootScope.token) {
        $http({
            url: '/api/user/auth',
            method: 'delete'
        }).success(function() {
            $rootScope.set_token = false;
            
            $location.path('/');
        })
    }
});

app.controller('PanelCtrl', function($scope) {
});

app.controller('UsersCtrl', function($scope) {
});