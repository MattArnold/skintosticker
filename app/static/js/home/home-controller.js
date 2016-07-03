angular.module('skintosticker')
  .controller('HomeController', ['$scope', function ($scope) {
  	$scope.orders = {};
    var ordersResponsePromise = $http.get('/admin/orders.json?=id,created_at,line_items');
    ordersResponsePromise.success(function(data) {
      $scope.orders = data.orders;
    }
  }]);
