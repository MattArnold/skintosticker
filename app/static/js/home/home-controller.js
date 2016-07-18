angular.module('skintosticker')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
    $scope.empty = false;
  	$scope.orders = {};
    var ordersResponsePromise = $http.get('/orders');
    ordersResponsePromise.success(function(data) {
      $scope.orders = data;
      if (!$scope.orders[0]){
        $scope.empty = true;
      }
    });
  }]);
