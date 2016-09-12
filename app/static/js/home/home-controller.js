angular.module('skintosticker')
  .controller('HomeController', ['$scope', '$http', '$sce', function ($scope, $http, $sce) {
    $scope.empty = false;
  	$scope.orders = {};
    $scope.printable = {};
    $scope.archives = {};

    error_data = {
      "character": "",
      "dt": "Error.",
      "fn": "",
      "id": "",
      "item": "",
      "label": "",
      "skin": "",
      "sticker": "",
      "cn": "",
    };

    var ordersResponsePromise = $http.get('/orders');
    ordersResponsePromise.success(function(data) {
      $scope.orders = data;
      if ($scope.orders[0]){
        $scope.printable = $scope.orders[0];
      } else {
        $scope.empty = true;
      };
    })
    .error(function(data) {
      $scope.orders = error_data;
    });

    var archivesResponsePromise = $http.get('/archives');
    archivesResponsePromise.success(function(data) {
      $scope.archives = data;
    })
    .error(function(data) {
      $scope.archives = error_data;
    });

    $scope.makePrintable = function() {
      $scope.printable = this.order;
    };

    $scope.print = function() {
      window.print();
      var fulfillmentPromise = $http.post('/fulfill/' + $scope.printable.id);
      console.log($scope.printable.id);
    };
  }]);
