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
            $rootScope.set_token(false);
            
            $location.path('/');
        })
    }
});

app.controller('PanelCtrl', function($scope, $http) {
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
    
    $scope.get_tasks();
    
    setInterval($scope.get_tasks, 1500);
});

app.controller('UsersCtrl', function($scope) {
});