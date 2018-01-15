// declare a module
var myAppModule = angular.module('latiApp', [])
.controller('Controller', ['$rootScope', '$scope', 'Service', function ($rootScope, $scope, service) {

        $scope.getModelUrl = function(id) {
            return $.nano(urls['model'], {id : id });
        };

        // Load tests from db based upon criteria
        $scope.remove = function(id) {
            service.remove($scope.criteria, function(ret){
                $scope.items = ret.data.items;
            });
        };

    }])
    .factory('Service', ['$http', function($http) {
        var service = {
            remove: function(params, success) {
                $http.post(urls['remove-rental'], params, {headers: {'Content-Type': 'application/json'} }).then(success);
            }
        };
        return service;
    }]);

