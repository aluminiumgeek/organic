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

app.controller('LogoutCtrl', function($scope, $rootScope, $http, $location, $cookieStore) {
    if ($rootScope.token) {
        $http({
            url: '/api/user/auth',
            method: 'delete'
        }).success(function() {
            $rootScope.set_token(undefined);
            $cookieStore.remove('token');
            $location.path('/');
        })
        
        clearInterval($rootScope.update_ticker);
    }
});

app.controller('PanelCtrl', function($scope, $rootScope, $http) {
    $scope.model = {
        items: []
    };
    
    $scope.append = function() {
        if ($scope.model.newitem) {
            $scope.model.items.push($scope.model.newitem);
            $scope.model.newitem = '';
        }
    }
    
    $scope.send = function() {
        if ($scope.model.items.length > 0) {
            $scope.task_sending = true;
        
            var data = {
                'items': $scope.model.items,
                'priority': 2
            };
        
            $http({
                url: '/api/task',
                method: 'post',
                data: data
            }).success(function(data) {
                if (data.status == 'ok') {
                    $scope.new_task_id = data.task_id;
                }
                
                $scope.clear();
                $scope.task_sending = false;
            });
        }
    }
    
    $scope.clear = function() {
        $scope.model.items = [];
        $scope.model.newitem = '';
    }
    
    $scope.create_user = function() {
        if ($scope.model.username && $scope.model.password) {
            $scope.creating_user = true;
            
            var params = {
                username: $scope.model.username,
                password: $scope.model.password,
                is_staff: $scope.model.is_staff ? '1' : '0'
            }
            
            console.log(params.is_staff);
                
            $http({
                url: '/api/users',
                method: 'post',
                data: utils.param(params)
            }).success(function(data) {
                console.log(data);
                $scope.creating_user = false;
                
                if (data.status == 'error') {
                    $scope.user_warning = data.msg;
                }
                else {
                    $scope.users.push({
                        username: $scope.model.username,
                        is_staff: $scope.model.is_staff
                    });
                    
                    $scope.model.username = '';
                    $scope.model.password = '';
                    $scope.model.is_staff = false;
                }
            })
        }
    }
    
    $scope.get_tasks = function() {
        $http({
            url: '/api/tasks',
            method: 'get',
        }).success(function(data) {
            data.tasks.map(function(item) {
                switch (item.status) {
                    case 1:
                        item.status_name = 'Waiting';
                        break;
                    case 2:
                        item.status_name = 'Success';
                        break;
                    case 3:
                        item.status_name = 'Error';
                        break;
                }
            });
            
            $scope.tasks = data.tasks;
        });
    }
    
    $scope.get_workers = function() {
        $http({
            url: '/api/workers',
            method: 'get'
        }).success(function(data) {
            $scope.workers = data.workers;
        })
    }
    
    $scope.get_users = function() {
        $http({
            url: '/api/users',
            method: 'get'
        }).success(function(data) {
            console.log(data);
            if (data.status == 'error') {
                console.log(data);
            }
            else {
                $scope.users = data.users;
            }
        })
    }
    
    $scope.get_tasks();
    $scope.get_workers();
    
    if ($rootScope.is_staff) {
        $scope.get_users();
    }
    
    $rootScope.update_ticker = setInterval(
        function() {
            $scope.get_tasks();
            $scope.get_workers()
        },
        1500
    );
});
