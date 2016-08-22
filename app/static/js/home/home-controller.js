angular.module('skintosticker')
  .controller('HomeController', ['$scope', '$http', '$sce', function ($scope, $http, $sce) {
    $scope.empty = false;
  	$scope.orders = {};
    $scope.printable = {};
    var ordersResponsePromise = $http.get('/orders');
    ordersResponsePromise.success(function(data) {
      $scope.orders = data;
      if (!$scope.orders[0]){
        $scope.empty = true;
      }
    });
    $scope.makePrintable = function() {
      $scope.printable = this.order;
    };
    $scope.print = function() {
      window.print();
    };
  }]);
