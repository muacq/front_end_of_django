var app = angular

    .module('myApp', ["ngCookies", "ngTagsInput", "infinite-scroll", "ngSanitize"])

    .controller('globalCtrl', function ($scope, $http, $state) {
        //TODO
    })

    .directive('browserAutocompleteForm', function() {
            return {
                priority: 10,
                link: function(scope, element, attrs) {
                    element.on('submit', function (ev) {
                        $('input[ng-model]', element).each(function (index, item) {
                            if (angular.element(this).attr('type') !== 'checkbox' && angular.element(this).attr('type') !== 'radio') {
                                angular.element(this).controller('ngModel').$setViewValue($(this).val());
                            }
                        });
                    });
                }
            };
        })

    .filter('trustHtml', function ($sce) {
         return function (input) {
            return $sce.trustAsHtml(input);
         }
    }).filter('ntobr', function(){
        return function(input){
            return input.replace(/\n/g,"<\/br>").replace(/ /g,"&nbsp;");
        };
    });



/*
app.factory('HttpInterceptor', function ($q, $injector) {
    return {
        request: function (config) {
            return config;
        },
        requestError: function (err) {
            return  (err);
        },
        response: function (res) {
            return res;
        },
        responseError: function (err) {
            var stateService = $injector.get('$state');
            if (-1 === err.status) {
                // 远程服务器无响应
            } else if (500 === err.status) {
                // alert(err.toString())
            } else if (404 === err.status) {
                // alert(err.toString())
            }
            // return $q.reject(err);
            return err;
        }
    };
});
*/
app.config(function ($interpolateProvider, $httpProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
        // Use x-www-form-urlencoded Content-Type
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        $httpProvider.defaults.headers.put['Content-Type'] = 'application/x-www-form-urlencoded';


        // Override $http service's default transformRequest
        $httpProvider.defaults.transformRequest = [function(data)
        {
          /**
           * The workhorse; converts an object to x-www-form-urlencoded serialization.
           * @param {Object} obj
           * @return {String}
           */
          var param = function(obj)
          {
              var query = '';
              var name, value, fullSubName, subName, subValue, innerObj, i;

              for(name in obj)
              {
                  value = obj[name];


                  if(value instanceof Array)
                  {
                      for(i=0; i<value.length; ++i)
                      {
                          subValue = value[i];
                          fullSubName = name + '[' + i + ']';
                          innerObj = {};
                          innerObj[fullSubName] = subValue;
                          query += param(innerObj) + '&';
                      }
                  }
                  else if(value instanceof Object)
                  {
                      for(subName in value)
                      {


                          subValue = value[subName];
                          if(subValue !== null){
                              // fullSubName = name + '[' + subName + ']';
                              //user.userName = hmm & user.userPassword = 111
                              fullSubName = name + '.' + subName;
                              // fullSubName =  subName;
                              innerObj = {};
                              innerObj[fullSubName] = subValue;
                              query += param(innerObj) + '&';
                          }
                      }
                  }
                  else if(value !== undefined ) //&& value !== null
                  {
                      query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
                  }
              }


              return query.length ? query.substr(0, query.length - 1) : query;
          };


          return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
        }];


        $httpProvider.defaults.useXDomain = true;
    // delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }
);