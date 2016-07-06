angular.module('skintosticker')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
  	$scope.orders = {};
  	$scope.test = 'Test!';
    var ordersResponsePromise = $http.get('/orders');
    ordersResponsePromise.success(function(data) {
      $scope.orders = data;
    });
  }]);
