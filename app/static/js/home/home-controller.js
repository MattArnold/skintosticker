angular.module('skintosticker')
  .controller('HomeController', ['$scope', '$http', function ($scope, $http) {
  	$scope.orders = {};
  	$scope.test = 'Test!';
    // var ordersResponsePromise = $http.get('/admin/orders.json?=id,created_at,line_items');
    var ordersResponsePromise = $http.get('/orders');
    ordersResponsePromise.success(function(data) {
      // angular.forEach(data, function(data){
      // 	//Decode a base64 string to an image
      //   var image = new Image();
      //   image.src = data.img;
      //   data.img = image;
      // });
      $scope.orders = data;
    });
  }]);
