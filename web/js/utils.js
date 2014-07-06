/*
 * Some utils
 * 
 */

utils = (function() {
    var self = {};
    
    self.param = function(a) {
        var s = [], add = function( key, value ) {
            s[ s.length ] = encodeURIComponent(key) + "=" + encodeURIComponent(value);
        };
        
        for (key in a) {
            add(key, a[key]);
        }
        
        // Return the resulting serialization
        return s.join("&").replace("%20", "+");
    }
    
    return self;
})();
